#include <stdio.h>

__global__ void sayHello() {
    printf("Hello world from the GPU!\n");
}

int main() {
   printf("Hello world from the CPU!\n");

   sayHello<<<1,1>>>();
   cudaDeviceSynchronize();
   
   return 0;
}
