# Determine installation path and install conda there
#installationPath=$(pwd)
installationPath=$HOME/temposeq_aligner_assets


# Modify script app.py
echo "#!$installationPath/conda/bin/python" > webapp.py
echo "executable_path = '$installationPath/conda/bin/'" >> webapp.py
cat app.py >> webapp.py
chmod +x webapp.py


echo "Script is ready"

# Make installation log file
touch ./source/installation.log

echo ""
echo "Checking Conda"
# Check if conda is already installed
if test -f "./source/conda/bin/conda"; then
    echo "Conda executable already present"
else
    echo "Installing miniconda"
    cd source
    echo $installationPath/conda
    bash Miniconda3-latest-Linux-x86_64.sh -b -p $installationPath/conda > installation.log 2>&1
    cd ../
    if test -f $installationPath/conda/bin/conda; then
        echo "Miniconda was installed successfully"
    else
        echo "An error has occurred while installing conda, please check the log file"
    fi
fi


echo ""
echo "Checking Dash and Pandas"
# Install dash and pandas with conda
$installationPath/conda/bin/pip install dash pandas >> ./source/installation.log
# Check if pandas and conda are installed correctly
$installationPath/conda/bin/pip list > pipList
if grep -Fq "dash" pipList; then
    echo "Dash was installed correctly"
else
    echo "Errors installing dash, please refer to log"
fi

if grep -Fq "pandas" pipList; then
    echo "Pandas was installed correctly"
else
    echo "Errors installing pandas, please refer to log"
fi
rm pipList



### Install Samtools, STAR, BWA, Kallisto, Subread and check they work

echo ""
echo "Checking Samtools"
# Start installing samtools
# Make a list of installed packages
$installationPath/conda/bin/conda list > condaList
if grep -Fq "samtools" condaList; then
    echo "Samtools was already installed"
else
    echo "Installing Samtools...."
    $installationPath/conda/bin/conda install -c bioconda -y samtools >> ./source/installation.log
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! this im not sure we do need
    cd $installationPath/conda/lib/
    ln -s librcrypto.so.1.1 libcrypto.so.1.0.0
    cd -

    # Check if it was installed
    $installationPath/conda/bin/conda list > condaList
    if grep -Fq "samtools" condaList; then
        echo "Samtools was installed successfully"
    else
        echo "Something went wrong while installing Samtools. Please check installation.log for details."
    fi
fi
rm condaList


echo ""
echo "Checking FeatureCount"
# Install featureCount (subread)
# Make a list of installed packages
$installationPath/conda/bin/conda list > condaList
if grep -Fq subread condaList; then
    echo "featureCount is already installed"
else
    echo "Installing featureCount...."
    $installationPath/conda/bin/conda install -c bioconda -y subread >> ./source/installation.log

    # Check if it was installed
    $installationPath/conda/bin/conda list > condaList
    if grep -Fq subread condaList; then
        echo "featureCount was installed successfully"
    else
        echo "Something went wrong while installing featureCount. Please check installation.log for details."
    fi
fi
rm condaList

# Install STAR
# Make a list of installed packages
$installationPath/conda/bin/conda list > condaList
echo ""
echo "Checking STAR"
if grep -Fq star condaList; then
    echo "STAR is already installed"
else
    echo "Installing STAR"
    $installationPath/conda/bin/conda install -c bioconda -y star >> ./source/installation.log
    
    # Check if installed successfully
    $installationPath/conda/bin/conda list > condaList
    if grep -Fq star condaList; then
        echo "STAR was installed successfully"
    else
        echo "Something went wrong while installing STAR. Please check installation.log for details."
    fi
fi
rm condaList


# Install BWA
$installationPath/conda/bin/conda list > condaList
echo ""
echo "Checking BWA"
if grep -Fq bwa condaList; then
    echo "BWA is already installed"
else
    echo "Installing BWA"
    $installationPath/conda/bin/conda install -c bioconda -y bwa >> ./source/installation.log
    
    # Check if installed successfully
    $installationPath/conda/bin/conda list > condaList
    if grep -Fq bwa condaList; then
        echo "BWA was installed successfully"
    else
        echo "Something went wrong while installing BWA. Please check installation.log for details."
    fi
fi
rm condaList



# Install Kallisto
$installationPath/conda/bin/conda list > condaList
echo ""
echo "Checking Kallisto"
if grep -Fq kallisto condaList; then
    echo "Kallisto is already installed"
else
    echo "Installing Kallisto"
    $installationPath/conda/bin/conda install -c bioconda -y kallisto >> ./source/installation.log
    
    # Check if installed successfully
    $installationPath/conda/bin/conda list > condaList
    if grep -Fq kallisto condaList; then
        echo "Kallisto was installed successfully"
    else
        echo "Something went wrong while installing Kallisto. Please check installation.log for details."
    fi
fi
rm condaList



















