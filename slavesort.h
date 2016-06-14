#ifndef SLAVESORT_H_LOCK
#define SLAVESORT_H_LOCK

void    slavesort(int* master, int* slave, int size);
void    ss_split(int* master, int* slave, int left, int right);
void    ss_merge(int* master, int* slave, int left, int mid, int right);

#endif
