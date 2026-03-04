//
// Created by omni on 3/4/26.
//

#include <stdio.h>
#include <string.h>

char stripIP[13];

char* cleanIP(char* ip) {
    // account for STRIP_IP=' -> 10 chars at the start
    ip+=10;

    // iterate until ' symbol found -> new sting end

}

int initEnv() {
    FILE* env = fopen("../.env", "r");
    if (env == NULL){return 1;}

    // read the first string from .env: at most: STRIP_IP='xyz.xyz.xyz.xyz'\n -> 27 chars
    char dirtyIP[27];
    fgets(dirtyIP, 28, env);


    return 0;
}


int initStripHandler() {
    if (initEnv()) {
        printf("ERR: Failed to initEnv.\n");
        return 1;
    }
    return 0;
}


