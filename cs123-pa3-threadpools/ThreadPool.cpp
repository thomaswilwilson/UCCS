/*
 * CMSC 12300 - Computer Science with Applications 3
 * Borja Sotomayor, 2013 (original code)
 * Matthew Wachs, 2016 (port to C)
 *
 * An implementation of the thread pool pattern.
 *
 * See ThreadPool.h for details.
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include "ThreadPool.h"
#include "WorkerThread.h"

// Use the next three functions to manipulate the queue of tasks maintained in the pool
// These use a linked list to represent a queue.

unsigned int queue_length(TaskQueue* q) {
    return q->length;
}

USAGovClickTask* queue_dequeue(TaskQueue* q) {
    if (q->head == NULL) {
        fprintf(stderr, "pop from empty queue\n");
        exit(1);
    }
    
    QueueEntry* qe = q->head;
    USAGovClickTask* rv = qe->task;
    
    q->head = qe->next;
    if (q->tail == qe) {
        q->tail = NULL;
    }
    q->length--;
    free(qe);
    
    return rv;
}

void queue_enqueue(TaskQueue* q, USAGovClickTask* task) {
    if (q->length >= MAX_TASKS) {
        fprintf(stderr, "attempt to push to full queue\n");
        exit(1);
    }
    
    QueueEntry* qe = (QueueEntry*)malloc(sizeof(QueueEntry));
    qe->task = task;
    qe->next = NULL;
    
    if (q->tail == NULL) {
        q->head = q->tail = qe;
    } else {
        q->tail->next = qe;
        q->tail = qe;
    }
    q->length++;
}

ThreadPool* pool_init(int numWorkers) {
    int i;
    ThreadPool* t = (ThreadPool*)malloc(sizeof(ThreadPool));
    t->numWorkers = numWorkers;
    t->workers = (WorkerThread**)malloc(sizeof(WorkerThread*)*numWorkers);
    t->on = false;
    pthread_mutex_init(&t->m, NULL);
    pthread_cond_init(&t->cvQueueNonEmpty, NULL);
    
    t->q = (TaskQueue*)malloc(sizeof(TaskQueue));
    t->q->length = 0;
    t->q->head = t->q->tail = NULL;
    
    for (i = 0; i < numWorkers; i++) {
        t->workers[i] = worker_init(t);
        worker_start(t->workers[i]);
    }
    
    return t;
}

void pool_free(ThreadPool* t) {
    unsigned int i;
    for (i = 0; i < t->numWorkers; i++) {
        worker_free(t->workers[i]);
    }
    
    while (queue_length(t->q)) {
        USAGovClickTask* task = queue_dequeue(t->q);
        task_free(task);
    }
    free(t->q);
    
    free(t);
}

bool pool_schedule(ThreadPool* t, USAGovClickTask* task) {
    /* YOUR CODE GOES HERE */
    
    unsigned int len = queue_length(t -> q);

    if (len < MAX_TASKS) {
        pthread_mutex_lock(&t->m);
        queue_enqueue(t -> q, task);
        pthread_cond_signal(&t->cvQueueNonEmpty);
        pthread_mutex_unlock(&t->m);
        return true;    
    }

    return false;
}

void pool_stop(ThreadPool* t) {
    /* YOUR CODE GOES HERE */

    t->on = true;
    pthread_cond_broadcast(&t->cvQueueNonEmpty);

    for (int i=0; i<t->numWorkers; i++) {
        void * ptr;
        pthread_join(t->workers[i]->thd, &ptr);
    }
    
}
