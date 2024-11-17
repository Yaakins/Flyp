#include "parsing.h"

AST_node *parse_int(char *str) {
  AST_node *res = malloc(sizeof(AST_node));
  res->type = INT_LIT;
  return res;
}

AST_node *parse(char *str) {
  AST_node *res = malloc(sizeof(AST_node));

  return res;
}
