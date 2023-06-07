#include <iostream>
#include <chrono>
#include <thread>
#include <fstream>

int main(int argc, char *argv[])
{
    using namespace std::this_thread;
    using namespace std::chrono;
    
    std::cout << "Given command line arguments: " << std::endl;
    for (int i = 1; i < argc; ++i)
    {
        std::cout << argv[i] << std::endl;
    }

    std::ofstream output_file;
    output_file.open ("example_output.txt");
        
    for (int i=0; i<120; i++)
    {
        sleep_for(seconds(1));
    
        std::cout << "Count: " << i << std::endl;
        output_file << i << "\n";
    }

    //output_file.close();

    std::cout << "Example program end." << std::endl;

    return 0;
}