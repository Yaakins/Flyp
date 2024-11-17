#include "resizable_array.h"

r_arr *create_arr(long initial_size, int element_size) {
  if (initial_size < 1 || element_size < 1) {
    errno = EINVAL;
    return NULL;
  }

  r_arr *res = malloc(sizeof(r_arr));
  res->allocated_length = initial_size;
  res->length = initial_size;
  res->element_size = element_size;
  res->data = malloc(initial_size * element_size);
   
  return res;
}

void destroy_arr(r_arr *target) {
  free(target->data);
  free(target);

  return;
}

int *append_i(r_arr *target, int n) {
  if (sizeof(int) != target->element_size) {
    errno = EINVAL;
    return NULL;
  }

  if (target->allocated_length == target->length) {
    void *new_data = malloc(target->length * 2 * target->element_size);
    memcpy(new_data, target->data, target->length);
    free(target->data);
    target->data = new_data;
    //target->data = realloc(target->data, target->length * 2);
    target->allocated_length = target->length*2;
  }
  ((int*)target->data)[target->length] = n;
  target->length++;
  return (int*)target->data + target->length;
}

int *set_i(r_arr *target, int n, int position) {
  if (sizeof(int) != target->element_size) {
    errno = EINVAL;
    return NULL;
  }

  if (position >= target->length || position < 0) {
    errno = EINVAL;
    return NULL;
  }
  ((int*)target->data)[position] = n;
  return (int*)target->data + position;
}

int get_i(r_arr *target, int position) {
  if (position >= target->length || position < 0) {
    errno = EINVAL;
    return 0;
  }
  int res = ((int*)target->data)[position];
  return res;
}

void *append(r_arr *target, void *element_addr, int element_size) {
  if (element_size != target->element_size) {
    errno = EINVAL;
    return NULL;
  }

  if (target->allocated_length == target->length) {
    void *old_data = target->data;
    void *new_data = malloc(target->length * 2 * target->element_size);
    target->data = memcpy(new_data, target->data, target->length * target->element_size);
    free(old_data);
    target->allocated_length = target->length*2;
    printf("Resized array from %d to %d elements\n", target->length, target->allocated_length);
  }
  memcpy(target->data + (target->element_size * target->length), element_addr, element_size);

  target->length++;
  return target->data + (target->element_size * target->length);
}

void remove_last(r_arr *target) {
  if (target->length != 0) {
    errno = EINVAL;
    return;
  }

  target->length--;
  return;
}
