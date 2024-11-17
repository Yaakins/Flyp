#include "resizable_array.h"

void print_array(r_arr *target) {
  printf("[");
  for (int i = 0; i < target->length - 1; i++) {
    printf("%d, ", get_i(target, i));
  }
  printf("%d]\n", get_i(target, target->length - 1));
  
  return;
}

int main() {
  r_arr *tab = create_arr(2, sizeof(int));

  set_i(tab, -14, 0);
  set_i(tab, 1892, 1);

  for (int i = 0; i < 10; i ++) {
    print_array(tab);
    append(tab, &i, sizeof(int));
  }

  print_array(tab);

  destroy_arr(tab);

  return 0;
}
