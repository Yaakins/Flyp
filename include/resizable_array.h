#ifndef _RESIZABLE_ARRAY_H_
#define _RESIZABLE_ARRAY_H_

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

typedef struct {
   int allocated_length;
   int length;
   int element_size;
   void *data;
}r_arr;

/* creates a resizable which contains `initial_size` elements
 * with each of them `element_size` bytes long
 * 
 * returns: a pointer to the created array struct
 */

r_arr *create_arr(long initial_size, int element_size);

/* Frees all the content of the array,
 * and the array itself
 */

void destroy_arr(r_arr *target);

/* appends an integer `n` at the end
 * of the array
 * Prefer to use append() instead
 */

int *append_i(r_arr *target, int n);

/* sets the value at index `position` to `n`
 * returns a pointer to the modified element
 */

int *set_i(r_arr *target, int n, int position);

/* returns the element at index `position`,
 * considered as an integer
 */

int get_i(r_arr *target, int position);

/* appends an element which is `element_size` bytes long,
 * and whose value is stored at address `element_addr`
 * returns a pointer to the modified element
 */

void *append(r_arr *target, void *element_addr, int element_size);

/* removes the last element of the array
 * If the array is empty, sets errno to EINVAL and returns
 */

void remove_last(r_arr *target);

#endif
