#include <iostream>
#include <chrono>
#include <thread>
#include <mpi.h>
#include <stdio.h>

int example()
{
    using namespace std::this_thread;
    using namespace std::chrono;
        
    for (int i=0; i<600; i++)
    {
        sleep_for(seconds(1));
    
        std::cout << "Count: " << i << std::endl;
    }
}

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Get the name of the processor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Print off a hello world message
    printf("Hello from processor %s, rank %d out of %d processors\n",
           processor_name, world_rank, world_size);

    MPI_Barrier(MPI_COMM_WORLD);

    example();

    MPI_Barrier(MPI_COMM_WORLD);

    printf("Ending from processor %s, rank %d out of %d processors\n",
           processor_name, world_rank, world_size);

    // Finalize the MPI environment.
    MPI_Finalize();

    std::cout << "Example program end."	<< std::endl;
}