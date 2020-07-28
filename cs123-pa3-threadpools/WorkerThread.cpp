/*
 * CMSC 12300 - Computer Science with Applications 3
 * Borja Sotomayor, 2013 (original code)
 * Matthew Wachs, 2016 (port to C)
 *
 * An implementation of the thread pool pattern.
 * This file contains the implementation of the worker threads
 *
 * See WorkerThread.h for details.
 */

#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include "ThreadPool.h"
#include <unistd.h>
#include "WorkerThread.h"

WorkerThread* worker_init(ThreadPool* pool) {
    WorkerThread* t = (WorkerThread*)malloc(sizeof(WorkerThread));
    
    t->pool = pool;

    return t;
}

void worker_free(WorkerThread* t) {
    free(t);
}

void worker_start(WorkerThread* t) {
    // Create the thread and make it run the run() function
    pthread_create(&t->thd, NULL, worker_run, (void*)t);
}

void* worker_run(void* tv) {
    WorkerThread* t = (WorkerThread*)tv;
    while (!t->pool->on) {
        // printf("queue_length: %d\n", queue_length(t->pool->q));

        pthread_mutex_lock(&t->pool->m);
        while (queue_length(t->pool->q)==0 && !t->pool->on) {
            pthread_cond_wait(&t->pool->cvQueueNonEmpty, &t->pool->m);
        }
        if (t->pool->on) {
            pthread_mutex_unlock(&t->pool->m);
            return NULL;
        }
        USAGovClickTask* task = queue_dequeue(t->pool->q);
        pthread_mutex_unlock(&t->pool->m);
        task_run(task);
    }
    // printf("%d\n", t->pool->on);
    return NULL;
}
