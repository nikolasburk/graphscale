from typing import Any

from graphscale.grapple.parser import parse_grapple, to_python_typename
from graphscale.grapple.pent_printer import (
    print_generated_pents_file_body,
    print_autopents_file_body,
)


def assert_generated_pent(snapshot: Any, graphql: str) -> None:
    grapple_document = parse_grapple(graphql)
    generated_output = print_generated_pents_file_body(grapple_document)
    snapshot.assert_match(generated_output)

    autopents_output = print_autopents_file_body(grapple_document)
    snapshot.assert_match(autopents_output)


def test_no_grapple_types(snapshot: Any) -> None:
    assert_generated_pent(snapshot, '''type TestObjectField {bar: FooBar}''')


def test_ignore_type(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''type TestObjectField @pent(typeId: 1000) {bar: FooBar} type Other { }'''
    )


def test_required_object_field(snapshot: Any) -> None:
    assert_generated_pent(snapshot, '''type TestObjectField @pent(typeId: 1000) {bar: FooBar!}''')


def test_object_field(snapshot: Any) -> None:
    assert_generated_pent(snapshot, '''type TestObjectField @pent(typeId: 1000) {bar: FooBar}''')


def test_required_field(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''type TestRequired @pent(typeId: 1000) {id: ID!, name: String!}'''
    )


def test_single_nullable_field(snapshot: Any) -> None:
    grapple_string = '''type Test @pent(typeId: 1) {name: String}'''
    grapple_document = parse_grapple(grapple_string)
    grapple_type = grapple_document.object_types()[0]
    assert grapple_type.name == 'Test'
    fields = grapple_type.fields
    assert len(fields) == 1
    name_field = fields[0]
    assert name_field.name == 'name'
    assert name_field.type_ref.graphql_typename == 'String'
    assert name_field.type_ref.python_typename == 'str'
    assert_generated_pent(snapshot, grapple_string)


def test_read_pent(snapshot: Any) -> None:
    assert_generated_pent(snapshot, '''type Query {
  todoUser(id: UUID!): TodoUser @readPent
 }''')


def test_browse_pent(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''type Query {
  allTodoUsers(first: Int = 100, after: UUID): [TodoUser!]! @browsePents
 }'''
    )


def test_stored_id_edge(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''type TodoUser @pent(typeId: 100000) {
  id: UUID!
  todoLists(first: Int = 100, after: UUID): [TodoList!]!
    @edgeToStoredId(
      edgeName: "user_to_list_edge"
      edgeId: 10000
      field: "owner"
    )
}

type TodoList @pent(typeId: 100002) {
  id: UUID!
  name: String!
  owner: TodoUser @genFromStoredId
}'''
    )


def test_generated_mutations(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''type Mutation {
  createTodoUser(data: CreateTodoUserData!): CreateTodoUserPayload @createPent
  updateTodoUser(id: UUID!, data: UpdateTodoUserData!): UpdateTodoUserPayload
    @updatePent
  deleteTodoUser(id: UUID!): DeleteTodoUserPayload @deletePent(type: "TodoUser")
}

input CreateTodoUserData @pentMutationData {
  name: String!
  username: String!
}

type CreateTodoUserPayload @pentMutationPayload {
  todoUser: TodoUser
}

input UpdateTodoUserData @pentMutationData {
  name: String
}

type UpdateTodoUserPayload @pentMutationPayload {
  todoUser: TodoUser
}

type DeleteTodoUserPayload @pentMutationPayload {
  deletedId: UUID
}
'''
    )


def test_merge_query_mutation(snapshot: Any) -> None:
    assert_generated_pent(
        snapshot, '''
type Query {
  todoUser(id: UUID!): TodoUser @readPent
}

type Mutation {
  createTodoUser(data: CreateTodoUserData!): CreateTodoUserPayload @createPent
}

input CreateTodoUserData @pentMutationData {
  name: String!
  username: String!
}

type CreateTodoUserPayload @pentMutationPayload {
  todoUser: TodoUser
}
 '''
    )


def test_graphql_type_conversion() -> None:
    assert to_python_typename('String') == 'str'
    assert to_python_typename('Int') == 'int'
    assert to_python_typename('SomeType') == 'SomeType'
