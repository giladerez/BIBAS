import pandas as pd
from pgmpy.inference import VariableElimination, CausalInference

def compute_bibas_pairwise(model, source, target, target_positive_state=1, operation="observe"):
    """
    Compute the BIBAS score from source → target (target must be binary).
    operation: 'observe' (default) uses inference; 'do' uses do-calculus (intervention)
    """
    try:
        source_cpd = model.get_cpds(source)
        target_cpd = model.get_cpds(target)

        if target_cpd.variable_card != 2:
            raise ValueError("Target must be binary")

        # Prior P(T=positive)
        infer = VariableElimination(model)
        prior = infer.query(variables=[target])
        p_t_pos = prior.values[target_positive_state]

        # Prior P(X=xi) for weighting
        p_x = infer.query(variables=[source]).values

        shifts = []
        for i in range(source_cpd.variable_card):
            if operation == "observe":
                posterior = infer.query(variables=[target], evidence={source: i})
                p_t_given_x = posterior.values[target_positive_state]

            elif operation == "do":
                doer = CausalInference(model)
                interventional = doer.do_inference(
                    query=target, do={source: i}
                )
                p_t_given_x = interventional.values[target_positive_state]

            else:
                raise ValueError("operation must be 'observe' or 'do'")

            shift = p_t_given_x - p_t_pos
            shifts.append(p_x[i] * abs(shift))

        return sum(shifts) * 100

    except Exception as e:
        return None


def rank_sources_for_target(model, target, target_positive_state=1, operation="observe"):
    """
    Ranks all source nodes by their BIBAS score on a given binary target.
    
    Parameters:
        model: pgmpy.models.DiscreteBayesianNetwork
        target: str – name of the target node (must be binary)
        target_positive_state: int – state of the target considered "positive"
        operation: 'observe' or 'do'
    
    Returns:
        pd.DataFrame with columns: ['source', 'bibas_score'], sorted descending
    """
    target_card = model.get_cpds(target).variable_card
    if target_card != 2:
        raise ValueError("Target must be binary")

    sources = [node for node in model.nodes() if node != target]

    rows = []
    for src in sources:
        score = compute_bibas_pairwise(
            model,
            source=src,
            target=target,
            target_positive_state=target_positive_state,
            operation=operation
        )
        rows.append({"source": src, "bibas_score": score})

    df = pd.DataFrame(rows).sort_values("bibas_score", ascending=False).reset_index(drop=True)
    return df