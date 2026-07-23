import flowkit as fk
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import re


def read_flow(directory):
    """
    Reads flow cytometry data from FCS files in specified directory.

    This function loads This function loads flow cytometry data from FCS files, processes them into a pandas DataFrame,
    and assigns tissue and condition labels based on sample IDs. It automatically detects conditions from the sample names.

    Parameters:
    ----------- 
    wsp_directory : str
        Path to the wsp file containing gating for FCS files.
    fcs_directory : str
        Path to the directory containing FCS files to be analyzed.

    Returns:
    -------- 
    tuple
        A tuple containing three elements:
        - df_flow (pandas.DataFrame): Combined DataFrame of all flow cytometry samples with added
          metadata columns (tissue, sample_id, condition).
        - sample_list (list): List of all sample IDs found in the directory.
        - wsp (flowkit.Workspace): The flowkit Workspace object containing gating and event information.

    """

    session = fk.Session(fcs_samples=directory)
    sample_list = session.get_sample_ids()

    df_flow = []
    for sample_id in sample_list:
        df = session.get_gate_events(sample_id)
        df['sample_id'] = (sample_id.split(' ')[1])
        df['tissue'] = (sample_id.split(' ')[2])
        df_flow.append(df)

    df_flow = pd.concat(df_flow)
    df_flow.columns = [pns if pns !=
                       '' else pnn for pnn, pns in df_flow.columns]

    new_cols = []
    for col in df_flow.columns:
        if ' : ' in col:
            marker = col.split(' ')[0]
            new_cols.append(marker)
        else:
            new_cols.append(col)

    df_flow.columns = new_cols

    print('Parameters:', df_flow.keys())
    return df_flow, sample_list


def pd_to_adata(df_flow, df_flow_counts):
    """
    Converts flow cytometry data from pandas DataFrames to an AnnData object.

    This function processes flow cytometry data and associated counts, creating an AnnData object
    with appropriate metadata. It truncates sample IDs, creates a metadata DataFrame, and assigns
    group and sample ID information to the AnnData object's observation annotations.

    Parameters:
    -----------
    df_flow : pandas.DataFrame
        A DataFrame containing flow cytometry data, including 'sample_id', 'condition', and 'tissue' columns.
    df_flow_counts : pandas.DataFrame
        A DataFrame containing count data for the flow cytometry samples.

    Returns:
    --------
    anndata.AnnData
        An AnnData object containing the flow cytometry count data with associated metadata.
        The object includes:
        - X: The count matrix from df_flow_counts
        - obs: Observation annotations including 'group' and 'sample_id'

    """

    if df_flow.isna().any().any():
        nan_cols = df_flow.columns[df_flow.isna().any()].tolist()
        raise ValueError(
            f"NaN values detected in df_flow columns: {nan_cols}"
        )

    df_flow['sample_id'] = df_flow['sample_id'].apply(lambda x: x[:4])
    list_metadata = {
        'sample_id': df_flow.sample_id,
        'tissue': df_flow.tissue
    }

    df_metadata = pd.DataFrame(list_metadata)
    adata = sc.AnnData(df_flow_counts)
    df_metadata.index = adata.obs.index

    for col in df_metadata.columns:
        adata.obs[col] = df_metadata[col]

    return adata
