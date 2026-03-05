//
// Created by omni on 3/4/26.
//

#include <stdio.h>
#include <string.h>

// max ipv4 length = 15 chars + \0
char stripIP[16];
char city[31];

char* cleanIP(char* ip) {
    // account for STRIP_IP=' -> 10 chars at the start
    ip+=10;

    // iterate until ' symbol found -> new sting end
    char* iterator = ip;
    while (*iterator != '\'') {
        iterator+=1;
    }
    *iterator = '\0';

    return ip;
}

// reads StripIP from .env file, cleans it and stores into StripIP varibale
int retrieveIP(FILE* env) {
    // read the first string from .env: at most: STRIP_IP='xyz.xyz.xyz.xyz'\n -> 27 chars
    // add \0 to terminate -> 28 chars
    char dirtyIP[28];
    fgets(dirtyIP, 28, env);

    char* cleanedIP = cleanIP(dirtyIP);
    strcpy(stripIP, cleanedIP);

    if (!*stripIP) {
        return 1;
    }

    return 0;
}

char* cleanCity(char* oldCity) {
    // account for CITY=' -> 6 chars
    oldCity+=6;

    // iterate until ' char found -> new string end
    char* iterator = oldCity;
    while (*iterator != '\''){iterator += 1;}
    *iterator = '\0';

    return oldCity;
}

int retrieveCity(FILE* env) {
    // max length of city 30 chars + 7 chars format + \0 -> 38 chars
    char dirtyCity[38];
    fgets(dirtyCity, 38, env);

    char* cleanedCity = cleanCity(dirtyCity);
    strcpy(city, cleanedCity);

    if (!*city){return 1;}

    return 0;
}

int initEnv(void) {
    FILE* env = fopen(".env", "r");
    if (env == NULL) {
        printf("ERR: Failed to open .env file.\n");
        return 1;
    }

    if (retrieveIP(env)) {
        printf("ERR: Failed to retrieve StripIP from .env.\n");
        return 1;
    }
    printf("IP retrieved successfully. StripIP: %s\n", stripIP);

    if (retrieveCity(env)) {
        printf("ERR: Failed to retrieve city from .env.\n");
        return 1;
    }
    printf("City retrieved successfully. City: %s\n", city);


    return 0;
}


int initDataHandler() {
    if (initEnv()) {
        printf("ERR: Failed to initEnv.\n");
        return 1;
    }
    return 0;
}


