#ifndef _PARSING_H_
#define _PARSING_H_

#include "resizable_array.h"
#include <stdlib.h>

enum AST_components {
  INT_LIT
};

typedef struct {
  int type;
  void *data1;
  void *data2;
} AST_node;

#endif
