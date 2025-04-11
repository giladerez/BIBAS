from pgmpy.inference import VariableElimination

def compute_bibas_pairwise(model, source, target):
    infer = VariableElimination(model)
    try:
        p1 = infer.query(variables=[target], evidence={source: 0}).values[1]
        p2 = infer.query(variables=[target], evidence={source: 1}).values[1]
    except:
        return None
    return abs(p1 - p2) * 100