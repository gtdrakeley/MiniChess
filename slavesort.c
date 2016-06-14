#include "slavesort.h"

#include <stdlib.h>



void    slavesort(int* master, int* slave, int size) {
    ss_split(master, slave, 0, size-1);
}


void    ss_split(int* master, int* slave, int left, int right) {
    if (left >= right) { return; }

    int mid = (left + right) / 2;
    ss_split(master, slave, left, mid);
    ss_split(master, slave, mid+1, right);
    ss_merge(master, slave, left, mid, right);
}


void    ss_merge(int* master, int* slave, int left, int mid, int right) {
    int size = right-left+1;
    int* merged_master = (int*)malloc(size*sizeof(int));
    int* merged_slave = (int*)malloc(size*sizeof(int));
    int i = 0;
    int l = left;
    int r = mid + 1;

    while (l <= mid && r <= right) {
        if (master[l] > master[r]) {
            merged_master[i] = master[r];
            merged_slave[i++] = slave[r++];
        } else {
            merged_master[i] = master[l];
            merged_slave[i++] = slave[l++];
        }
    }
    while (l <= mid) {
        merged_master[i] = master[l];
        merged_slave[i++] = slave[l++];
    }
    while (r <= right) {
        merged_master[i] = master[r];
        merged_slave[i++] = slave[r++];
    }
    for (int j=0; j<size; ++j) {
        master[left+j] = merged_master[j];
        slave[left+j] = merged_slave[j];
    }

    free(merged_master);
    free(merged_slave);
}
