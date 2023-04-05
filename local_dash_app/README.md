# Local Aligner Webapp GUI

### Installation
In order to install the environment for the GUI on Windows, you will need WSL installed. If you already completed this requirement, please skip the next point.

*Extra - Install WSL*
Guide on installing wsl....

*Run the install.sh script*
- Open an instance of WSL terminal. Move to the tool directory eg `cd local_dash_app`.
- Run the installing script eg `bash install.sh`

*Inspect the installation.log*
After all the installation steps are completed, make sure all processes run correctly by inspetting the installation.log file inside the source folder. If no error messages are present, the app can be run!


### Usage
In order to run the app, you will need a WSL terminal instance and a web browser (Google Chrome is the recommended one to avoid aestethic issues).

In the WSL terminal, move to the tool directory eg `cd local_dash_app`, and simply run `./webapp`. At this point, you should see a message in the WSL terminal saying that the server is running on port 3000. At this point you can open the web browser and go to the address http://127.0.0.1:3000/. 

The interface allows you to select a reference genome, the aligner of choice (between STAR, BWA and Kallisto), the number of allowed mismatches (only if using the aligner STAR), the number of threads to be used (STAR has limitations due to memory usage per thread), the output name and the files of interest. 

In order to load the fastq files to be aligned, simply drag a folder with the reads inside the *my_reads* folder. The webapp will allow you to store multiple folders inside the my_reads directory for future use. Once the alignment is complete, a new folder called *aligned* will be created in my_reads. The folder aligned is the output folder, where a directory is created for each experiment, and a directory specific for each experiment in turn. The webapp outputs 3 files, the read count, the mapped unmapped metadata and the run log file. 


### Advanced users only
The webapp creates a directory named temposeq_aligner_assets in your $HOME path. In order to completely remove any trace of the app, you should delete that folder too (it contains all the conda executables)
