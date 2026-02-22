//
// Created by omni on 2/22/26.
//
#include <stdio.h>
#include <pthread.h>


// initializes grpc
void* initAPI(void* arg) {
    return NULL;
}

void* initCheck(void* arg) {
    return NULL;
}

// does a singular check, return 0 on success
int check() {

    return 0;
}

int runCLI() {

    return 0;
}


int main(int argc, char* argv[]) {
    printf("Launching application.\n");

    // spawn threads to do the work for you
    pthread_t apiThread;
    if(pthread_create(&apiThread, nullptr, initAPI, NULL)) {
        printf("ERR: Failed to init api thread.\n");
    } else{printf("API thread created successfully.\n");}

    pthread_t checkThread;
    if(pthread_create(&checkThread, nullptr, initCheck, NULL)) {
        printf("ERR: Failed to init check thread.\n");
    }else{printf("Check thread created successfully.\n");}

    printf("Application initialization finished.\n");

    pthread_join(apiThread, nullptr);
    pthread_join(checkThread, nullptr);

    printf("All the threads have finished.\n");

    return 0;
}