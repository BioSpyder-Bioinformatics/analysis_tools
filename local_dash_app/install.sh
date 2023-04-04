# Determine installation path and install conda there
installationPath=$(pwd)

# Make installation log file
touch ./source/installation.log

# Check if conda is already installed
if test -f "./source/conda/bin/conda"; then
    echo "Anaconda executable already present"
else
    echo "Installing miniconda"
    cd source
    bash Miniconda3-latest-Linux-x86_64.sh -b -p ./conda >> installation.log 2>&1
    cd ../
    if test -f "./source/conda/bin/conda"; then
        echo "Miniconda was installed successfully"
    else
        echo "An error has occurred while installing conda, please check the log file"
    fi
fi


# Install dash and pandas with conda
./source/conda/bin/pip install dash pandas >> ./source/installation.log
echo "Installed dash and pandas"
echo " "

### Install Samtools, STAR, BWA, Kallisto, Subread and check they work

# Start installing samtools
# Make a list of installed packages
./source/conda/bin/conda list > condaList
if grep -Fq "samtools" condaList; then
    echo "Samtools was already installed"
else
    echo "Installing Samtools...."
    ./source/conda/bin/conda install -c bioconda -y samtools >> ./source/installation.log
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! this im not sure we do need
    # cd source/conda/lib/
    # ln -s librcrypto.so.1.1 libcrypto.so.1.0.0
    # cd ../../../

    # Check if it was installed
    ./source/conda/bin/conda list > condaList
    if grep -Fq "samtools" condaList; then
        echo "Samtools was installed successfully"
    else
        echo "Something went wrong while installing Samtools. Please check installation.log for details."
    fi
fi
rm condaList


# Install featureCount (subread)
# Make a list of installed packages
./source/conda/bin/conda list > condaList
if grep -Fq subread condaList; then
    echo "featureCount is already installed"
else
    echo "Installing featureCount...."
    ./source/conda/bin/conda install -c bioconda -y subread >> ./source/installation.log

    # Check if it was installed
    ./source/conda/bin/conda list > condaList
    if grep -Fq subread condaList; then
        echo "featureCount was installed successfully"
    else
        echo "Something went wrong while installing featureCount. Please check installation.log for details."
    fi
fi
rm condaList

# Install STAR
# Make a list of installed packages
./source/conda/bin/conda list > condaList
echo ""
echo "Checking STAR"
if grep -Fq star condaList; then
    echo "STAR is already installed"
else
    echo "Installing STAR"
    ./source/conda/bin/conda install -c bioconda -y star >> ./source/installation.log
    
    # Check if installed successfully
    ./source/conda/bin/conda list > condaList
    if grep -Fq star condaList; then
        echo "STAR was installed successfully"
    else
        echo "Something went wrong while installing STAR. Please check installation.log for details."
    fi
fi
rm condaList


# Install BWA
./source/conda/bin/conda list > condaList
echo ""
echo "Checking BWA"
if grep -Fq bwa condaList; then
    echo "BWA is already installed"
else
    echo "Installing BWA"
    ./source/conda/bin/conda install -c bioconda -y bwa >> ./source/installation.log
    
    # Check if installed successfully
    ./source/conda/bin/conda list > condaList
    if grep -Fq bwa condaList; then
        echo "BWA was installed successfully"
    else
        echo "Something went wrong while installing BWA. Please check installation.log for details."
    fi
fi
rm condaList



# Install Kallisto
./source/conda/bin/conda list > condaList
echo ""
echo "Checking Kallisto"
if grep -Fq kallisto condaList; then
    echo "Kallisto is already installed"
else
    echo "Installing Kallisto"
    ./source/conda/bin/conda install -c bioconda -y kallisto >> ./source/installation.log
    
    # Check if installed successfully
    ./source/conda/bin/conda list > condaList
    if grep -Fq kallisto condaList; then
        echo "Kallisto was installed successfully"
    else
        echo "Something went wrong while installing Kallisto. Please check installation.log for details."
    fi
fi
rm condaList



















