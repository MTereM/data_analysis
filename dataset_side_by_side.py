import ipywidgets as widgets
print_header = lambda msg: print(f"{msg}\n{'-'*len(msg)}")

def dataset_side_by_side(dataset1,title_dataset1,dataset2,title_dataset2,dataset3,title_dataset3):
    dataset1_out = widgets.Output()
    dataset2_out = widgets.Output()
    dataset3_out = widgets.Output()
    

    with dataset1_out:
        print_header(title_dataset1)
        display(dataset1)
        
    with dataset2_out:
        print_header(title_dataset2)
        display(dataset2)
    
    with dataset3_out:
        if (dataset3 is None) & (title_dataset3 is None):
            display()
        else:
            #print_header(' ')
            print_header(title_dataset3)
            display(dataset3)
            
    hbox = widgets.HBox([dataset1_out,dataset2_out,dataset3_out])
    display(hbox)