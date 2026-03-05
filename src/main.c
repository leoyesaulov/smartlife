//
// Created by omni on 2/22/26.
//
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#include "../include/dataHandler.h"

// Initializes data such as global vars before the application start. Returns 0 on success.
int initData(void) {
    printf("Initializing data.\n");


    return 0;
}

// initializes grpc
void* initAPI(void* arg) {
    printf("API thread started.\n");

    return NULL;
}

// does a singular check, return 0 on success
int check(void) {
    printf("Check has been performed.\n");
    return 0;
}

void checkLoop(void) {
    while (1) {
        // check if we should turn the lights on or off
        check();
        // sleep for 60 secs before the next check
        sleep(3);
    }
}

void* initCheck(void* arg) {
    printf("Check thread started.\n");
    checkLoop();

    return NULL;
}

int runCLI(void) {

    return 0;
}


int main(int argc, char* argv[]) {
    printf("Launching application...\n");

    if (initDataHandler()) {
        printf("ERR: Data initialization failed.\nAborting...\n");
        return 1;
    }

    // spawn threads to do the work for you
    pthread_t apiThread;
    if(pthread_create(&apiThread, nullptr, initAPI, NULL)) {
        printf("ERR: API initialization failed.\nAborting...\n");
        return 1;
    }

    pthread_t checkThread;
    if(pthread_create(&checkThread, nullptr, initCheck, NULL)) {
        printf("ERR: Check-Loop initialization failed.\nAborting...\n");
        return 1;
    }

    printf("Application initialization finished.\n");

    pthread_join(apiThread, nullptr);
    pthread_join(checkThread, nullptr);

    printf("All the threads have finished.\n");

    return 0;
}