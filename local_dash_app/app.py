import dash
from dash import Dash, dcc, html, Output, Input, State, callback, dash_table
import os
import pandas as pd
from assets.align_files_local import run_aligner
import subprocess
import multiprocessing
from assets.components import *

# Helper functions
def get_reference_list():
    #this_dir = os.getcwd()
    # Get path of this file
    this_file = os.path.realpath(__file__)
    # From file path get relative directory
    this_dir = this_file.removesuffix(os.path.basename(this_file)) # removes this filename from path
    files = os.listdir(fr'{this_dir}assets/references/')
    files = [file.removesuffix('.fa').removeprefix('TempO-Seq_') for file in files if file.split('.')[-1] == 'fa']
    return files

def get_path_from_reference(reference):
    # Get path of this file
    this_file = os.path.realpath(__file__)
    # From file path get relative directory
    this_dir = this_file.removesuffix('app.py')
    return_path = fr'{this_dir}assets/references/TempO-Seq_{reference}.fa'
    return return_path


# Helper functions
def get_local_files_path():
    #this_dir = os.getcwd()
    # Get path of this file
    this_file = os.path.realpath(__file__)
    # From file path get relative directory
    this_dir = this_file.removesuffix(os.path.basename(this_file)) # removes this filename from path
    directory = fr'{this_dir}my_reads/'
    return directory



dash_app = dash.Dash(__name__, prevent_initial_callbacks=True,)


# Need to: prompt them to select a folder
# Only give them so many reference genomes, can look from local app!
# Number of threads = max number of threads of their computer -1
# Remove email
# Give option to select output folder (tick mark if same as input)



# Set stylesheets
dash_app.config.external_stylesheets = ['./dash_assets/style/base_style.css', './dash_assets/style/additional_style.css']

raw_reads_directory = get_local_files_path()
aligned_complete_directory = raw_reads_directory + 'aligned/'

# Make aligned folder if not already present 
if not os.path.isdir(aligned_complete_directory):
    os.mkdir(aligned_complete_directory)


# Find directories with fastqfiles
try:
    directories = os.listdir(raw_reads_directory)
    directories.remove('aligned') 
except:
    directories = ['No directories found', 'Please contact support']


references = get_reference_list()

# Declare aligners options
aligners = {'star':'STAR', 'bwa': 'BWA', 'kallisto':'Kallisto'}

# Get number of processors
processors = multiprocessing.cpu_count()
# Threads are now up to available-2
threads = [x for x in range(1, processors-2)]


# dash_app layout
dash_app.layout = html.Div([
        # Card wrapper encloses the whole page 
        genericCardWrapper(
            [   
                genericInputWrapper(
                    dcc.Markdown('### Select your FASTA reads and parameters to continue'), 
                    style={'margin':'auto'}
                ),
                # Elements:
                # Two sections
                # Section 1 - Dropdown of folders, Table to pick the files
                # Section 2 - Dropdown (reference_genome, aligner, mismatches, threads) - Text input (Email, Output name)
                
                ############ Pick options:
                html.Div(
                    [
                        html.Div( #First section
                            [
                                # Select folder
                                genericInputWrapper([
                                    'Please select a folder:',
                                    dcc.Dropdown(
                                    options= directories,
                                    value=directories[0],
                                    id='dropdown_pick_folder_aligner',
                                    style={'width': '30rem'}
                                    )
                                ]),
                                # Select file
                                genericInputWrapper([
                                    #Div for button  
                                    SubmitButtonComponentAIO('Select/Deselect All', size='s', aio_id='select_deselect_button'),

                                    # Create an empty data table that just sits there for the callback to be linked to it (actual one in callback)
                                    html.Div(
                                        dash_table.DataTable(
                                            id = 'pick_file_data_table',
                                            style_table={'display':'none'}
                                        ), 
                                        id='table_pick_files_aligner', style={'width':'inherit'})

                                ] 
                                )
                                

                            ],className='six columns', style={'display': 'grid', 'gridTemplateRows': '1fr 5fr'}
                        ),
                        html.Div(# Second section
                            [
                                # Reference genome
                                genericInputWrapper([
                                    'Please select the reference genome:',
                                    dcc.Dropdown(
                                    options= references,
                                    #['Genome_X', 'Genome_Y'],
                                    id='dropdown_aligner_reference_genome',
                                    style={'width': '30rem'}
                                    )
                                ]),
                                # Aligner
                                genericInputWrapper([
                                    'Please select the preferred aligner: ',
                                    dcc.Dropdown(
                                    options=aligners,
                                    id='dropdown_aligner_aligner_software',
                                    style={'width': '20rem'}
                                    )
                                ]),
                                # Mismatches
                                genericInputWrapper([
                                    'Please select the number of allowed mismatches (STAR only): ',
                                    dcc.Dropdown([0, 1, 2, 3],
                                    value=2,
                                    id='dropdown_aligner_allowed_mismatches',
                                    style={'width': '20rem'}
                                    )
                                ]),
                                # Threads
                                genericInputWrapper([
                                    'Please select the number of threads: ',
                                    dcc.Dropdown(threads,
                                    id='dropdown_aligner_number_threads',
                                    style={'width': '20rem'},
                                    value=8
                                    )
                                ]),
                                # Output name
                                genericInputWrapper([
                                    'Please enter the output name: ',
                                    dcc.Input(type='text', placeholder='Output name',
                                    id='output_name_aligner', 
                                    style={'width': '25rem'})
                                ]),
                                genericInputWrapper([
                                    'Additional comments: ',
                                    dcc.Input(
                                        placeholder='Comments',
                                        id='aligner_additional_comments',
                                        style={'width': '95%'}
                                    )
                                ]) 


                        ], className='six columns flexer'
                        ), 


                ], className='row'
                ),# Top level wrapper container of the two 'section' wrappers
                
                
                
            



                # Submit button
                html.Div(SubmitButtonComponentAIO(
                    'Start Alignment',
                    aio_id='start_alignment_btn'
                    ),
                    className='flexer'
                    ),

                # Div for updating the user on the status 
                html.Div(id='start_alignment_div_status', style={'whiteSpace': 'pre-wrap'}),
            ]
        ),

        # All the required stores/connections to kevin to check if there are complete alignments
        # Complete alignments can have a file in the folder that flags the end of the run!!!
        


    ],
    className='mainDivPageGeneric'
    )
        


# Callback to populate the files table
@callback(
    Output('table_pick_files_aligner', 'children'),
    Input('dropdown_pick_folder_aligner', 'value')
)
def return_files(folder):
    try:
        files = os.scandir(f'{raw_reads_directory}/{folder}')
    except:
        return genericInputWrapper([
            'Please select a directory'
            ], style={'width': '80%'})

    # byte to Gb
    byte_to_gb = lambda x: round(float(x)/1000000000, 3)

    # Create dict with info
    dictionary = {}
    # index = 0
    for entry in files:
        if entry.is_file() and (entry.name.endswith('gz') or entry.name.endswith('fastq')):
            dictionary[entry.name] = [entry.name, byte_to_gb(entry.stat().st_size)]
            # index += 1
    # convert dict to df
    df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Filename', 'Size (Gb)'])
    #print(df)
    dt = dash_table.DataTable(
        id = 'pick_file_data_table',
        columns=[
            {'name': i, 'id':i, 'deletable':False, 'selectable':True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        row_selectable='multi',
        page_size=12,
        # Put text on left
        style_cell_conditional=[
            {
                'if': {
                    'column_id': 'Filename'
                },
                'textAlign': 'left'
            }
        ]
    )

    return dt
    



# Select deselect all callback
@callback(
    Output('pick_file_data_table', 'selected_rows'),    
    Input(SubmitButtonComponentAIO.ids.button('select_deselect_button'), 'n_clicks'),
    State('pick_file_data_table', 'selected_rows'),    
    State('pick_file_data_table', 'data'),  
    prevent_initial_call = True  
)
def select_deselect(clicks, selection, data):
    # basically if there is anything selected return empty array, else return array with all numbers for how long the data is 
    if selection == None:
        return [x for x in range(len(data))] 
    if len(selection) > 0:
        return [] 
    else:
        return [x for x in range(len(data))] 





# Callback for download button
@callback(
    Output('start_alignment_div_status', 'children'),
    Input(SubmitButtonComponentAIO.ids.button('start_alignment_btn'), 'n_clicks'),
    State('dropdown_aligner_reference_genome', 'value'),
    State('dropdown_aligner_aligner_software', 'value'),
    State('dropdown_aligner_allowed_mismatches', 'value'),
    State('dropdown_aligner_number_threads', 'value'),
    State('output_name_aligner', 'value'),
    State('pick_file_data_table', 'selected_rows'),
    State('pick_file_data_table', 'data'),
    State('dropdown_pick_folder_aligner', 'value'),
    State('aligner_additional_comments', 'value'),
    prevent_initial_call=True
)
def start_alignment(clicks, genome, aligner, mismatches, threads, output_name, selection, files, directory, comments):
    genome = get_path_from_reference(genome)
    print(clicks, genome, aligner, mismatches, threads, output_name, selection, directory, comments)
    # Missing - input_directory, output_name, zipped?, specific files?
    
    # Check which compulsory fields are missing (genome, aligner, files)
    missing = []

    # Check for genome
    if genome == None:
        missing.append('Genome')
    

    # Check if aligner is selected
    if aligner == None:
        missing.append('Aligner')

    # Check if directory is selected
    if directory == None:
        missing.append('Directory')
    else:# Add complete path
        complete_directory = f'{raw_reads_directory}{directory}'

    # get files
    selected = []
    if selection != None and len(selection) > 0:
        for sel in selection:
            selected.append(files[sel]['Filename'])
    else:
        missing.append('Files')

    # Check name of file
    if output_name == None:
        missing.append('Output name')
    else:
        # exchange spaces for underscores if any  
        if ' ' in output_name:
            output_name = output_name.strip()
            output_name = output_name.replace(' ', '_')
        #check if the filename is already present in the destination folder
        if os.path.exists(f'{aligned_complete_directory}/{directory}/{output_name}_count_table.csv'):
            return genericInputWrapper('Please choose a different output name to avoid overwriting', className='warning')
        if os.path.exists(f'{aligned_complete_directory}/{directory}/{output_name}'):
            return genericInputWrapper('An alignment with the same name is currently running, please choose a different output name to avoid overwriting', className='warning')


    # If any of the compulsory fields is missing, let the user know!
    if len(missing) > 0:
        s = f"Field{'s' if len(missing)>1 else ''} missing: " +  ', '.join(missing)
        return genericInputWrapper(s, className = 'warning')

    # Fallback for non compulsory fields:
    mismatches = mismatches or 2

    threads = threads or 2

    #feed a directory where to move the files once done 
    output_directory = f'{aligned_complete_directory}{directory}'

    ###run_aligner(aligner, reference_index, current_directory, file_list, output_name, email=None, threads=8, mismatches = 2):
    # run_aligner(aligner, genome, directory, selected, output_name, email, threads, mismatches)
    
    # Launch aligner with threading so it doesn't freeze the other processes
    #threading.Thread(target=run_aligner, args=[aligner, genome, complete_directory, selected, output_name, output_directory, email, threads, mismatches]).start()
    
    script_path = os.path.abspath(os.getcwd() + '/assets/' )
    print(f'python {script_path}/align_files_local.py -a {aligner} -g {genome} -i {complete_directory} -f {",".join(selected)} -o {output_name} -d {output_directory} -t {threads} -m {mismatches}')

    #subprocess.Popen(f'python {script_path}/align_files_local.py -a {aligner} -g {genome} -i {complete_directory} -f {",".join(selected)} -o {output_name} -d {output_directory} -t {threads} -m {mismatches}', shell=True)

    return_string = f"""Your alignment started with the following parameters:
    - Aligner: {aligner}
    - Genome: {genome} 
    - Selected directory: {complete_directory}
    - Number of selected files: {len(selected)}
    - Output prefix: {output_name}"""

    return genericInputWrapper(return_string)

    # make subprocess instead of threading when starting new one, or deepcopy of run_aligner function













# Run dash_app
if __name__ == '__main__':
    dash_app.run_server(port=3000, debug=True) 
