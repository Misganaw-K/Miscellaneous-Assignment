#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <stdlib.h>

int main(){



    int shm_id;
    size_t size = sizeof(char)*26;
    int shmflg = IPC_CREAT | 0666;

    key_t key = 12345;
    char *char_value;

    shm_id = shmget(key, size, shmflg);
    if(shm_id == -1){
        perror("ERROR: shmget has failed\n");
        exit(0);
    }
    char_value = shmat(shm_id, NULL, 0);
    if(char_value == (char*)-1){
        perror("ERROR: shmat has failed\n");
        exit(0);
    }

    printf("The value stored by the first process is %s\n", char_value);

    printf("The ASCI value of the letters are:\n");
    
    for(int i=0;i<26;i++){
        printf("%d ",(int)*(char_value+i));
    }
    printf("\n");

    *char_value = 'B';
    
    

    if(shmdt(char_value) == -1){
        perror("ERROR: shmdt has failed \n");
    }

    shmctl(shm_id,IPC_RMID,NULL);

    return 0;
}
