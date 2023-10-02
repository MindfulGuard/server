def concatenate_with_dot(*args)->str:
    """
    Params:
        N0:str,N1:str,Nn,...Nn-1
    Return:
        string(N0+"."+N1,...,Nn+"."+Nn-1)
    """
    result = ".".join(args)
    return result