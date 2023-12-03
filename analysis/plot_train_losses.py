import re
import matplotlib.pyplot as plt
import ast
import pandas as pd

def extract_losses_epoch_end(line):
    match = re.search(r'(\{.*\})', line)
    if match:
        epoch_info_str = match.group(1)
        epoch_info = ast.literal_eval(epoch_info_str)
        return epoch_info.get('train_loss'), epoch_info.get('val_loss')
    
    else:
        return None

def plot_losses(train_losses, val_losses, emb_type):
    # create figure
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Train and Validation Loss Over Epochs')
    plt.legend()
    
    # save figure
    filename = f"./figures/{emb_type}_losses.png"
    plt.savefig(filename)

def save_csv(train_losses, val_losses, emb_type):
    # convert loss values to dictionary
    losses_dict = {"train": train_losses, "val": val_losses}
    losses_df = pd.DataFrame(losses_dict)

    # define filename
    filename = f"./data/{emb_type}_losses.csv"
    losses_df.to_csv(filename)

def main(out_file, emb_type):

    # open file and read
    with open(out_file, 'r') as file:
        lines = file.readlines()

    # loop through all lines and store loss values
    train_losses = []
    val_losses = []
    for line in lines:
        losses = extract_losses_epoch_end(line)
        if losses is not None:
            train_loss, val_loss = losses
            if train_loss < 2.5 and val_loss < 2.5:
                train_losses.append(train_loss)
                val_losses.append(val_loss)

    # save csv files
    plot_losses(train_losses = train_losses, val_losses = val_losses, emb_type=emb_type)
    save_csv(train_losses=train_losses, val_losses=val_losses, emb_type = emb_type)
    
if __name__ == "__main__":

    # define out files
    OHE_OUT = "run_train_eigenfold_one_hot.out"
    OMEGA_OUT = "run_train_eigenfold.out"
    TYPE = "ohe" # change

    # out files dictionary
    out_files = {"ohe": OHE_OUT, "omegafold": OMEGA_OUT}

    # define arguments for filepath and csv/loss files
    out_file = f"../out/{out_files[TYPE]}"  # Replace with the actual path to your log file
    
    main(out_file=out_file, emb_type = TYPE)
