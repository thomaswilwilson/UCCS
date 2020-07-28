/*
 * CMSC 12300 - Computer Science with Applications 3
 * Borja Sotomayor, 2013 (original code)
 * Matthew Wachs, 2016 (port to C)
 *
 * USAGovClickData is a simple struct that aggregates data
 * about multiple 1.usa.gov clicks.
 *
 * See USAGovClickData.h for details
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include "USAGovClickData.h"

USAGovClickData* data_init() {
    USAGovClickData* t = (USAGovClickData*)malloc(sizeof(USAGovClickData));
    t->numClicks = 0;
    t->numNew = 0;
    
    return t;
}

void data_free(USAGovClickData* t) {
    free(t);
}

pthread_mutex_t accum_mutex = PTHREAD_MUTEX_INITIALIZER;

void data_update(USAGovClickData*t, USAGovClick* click) {
    pthread_mutex_lock(&accum_mutex);
    t->numClicks++;
    if (!click->known) {
        t->numNew ++;
    }
    pthread_mutex_unlock(&accum_mutex);

    
    
}
