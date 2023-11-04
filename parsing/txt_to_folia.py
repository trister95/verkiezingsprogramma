import os
import ucto
import tqdm

def list_txt_files(directory):
    return [filename for filename in os.listdir(directory) if filename.endswith('.txt')]

def txt_to_folia(input_dir, output_dir):
    """
    Tokenizes txt files by converting them to folia.xml-files.
    """
    configurationfile_ucto = "tokconfig-nld" 
    tokenizer = ucto.Tokenizer(configurationfile_ucto, foliaoutput = True)

    for f in tqdm.tqdm(list_txt_files(input_dir), desc = "looping through text files"):
        p = input_dir + "/" + f
        out_path = str(output_dir) + "/" + f.split(".")[0] + ".folia.xml"
        if not os.path.exists(out_path):
            tokenizer.tokenize(p, out_path)
    return