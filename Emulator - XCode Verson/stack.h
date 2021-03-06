#ifndef STACK_H_INCLUDED
#define STACK_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include "constants.h"

#include "dataTypes.h"
#include "data.h"


void s_push(struct Stack* stack, struct Data data)
{

    if (stack->index + 1 >= stack->size)
    {
        // double size of array
        stack->size *= 2;
        stack->arr = realloc(stack->arr, stack->size * sizeof (struct Data));
    }

    // push to the top of stack, 
    stack->arr[++stack->index] = data;
}

int s_empty (struct Stack* stack)
{
    // check if stack is empty
    return stack->index == -1;
}


void s_pop(struct Stack* stack)
{

    // For testing, remove for efficiency.
    // free_data(&stack->arr[stack->index]);
    stack->index -= 1;
}

void s_init(struct Stack* stack, int size)
{
    stack->size = size;
    stack->index = -1;
    stack->arr = malloc(size * sizeof(struct Data));
}



struct Data s_top(struct Stack* stack)
{
    if (s_empty(stack)) {
        //printf("STAC EMPYU AT TOP\n");
    }
    return stack->arr[stack->index];
}

//void s_free(struct Stack* stack)
//{
//    for (int i = 0; i < stack->size; i++) {
//        free_data(&stack->arr[i]);
//    }
//    free(stack->arr);
//    stack->size = -1;
//    stack->index = -1;
//}

#endif // STACK_H_INCLUDED
