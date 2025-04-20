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
        prior_infer = VariableElimination(model)
        prior = prior_infer.query(variables=[target])
        p_t_pos = prior.values[target_positive_state]

        # Prior P(X=xi) for weighting
        p_x = prior_infer.query(variables=[source]).values

        # Choose inference engine
        if operation == "observe":
            infer = prior_infer
        elif operation == "do":
            infer = CausalInference(model)
        else:
            raise ValueError("operation must be 'observe' or 'do'")

        shifts = []
        for i in range(source_cpd.variable_card):
            if operation == "observe":
                posterior = infer.query(variables=[target], evidence={source: i})
                p_t_given_x = posterior.values[target_positive_state]
            elif operation == "do":
                interventional = infer.query(variables=[target], do={source: i})
                p_t_given_x = interventional.values[target_positive_state]

            shift = abs(p_t_given_x - p_t_pos)
            shifts.append(p_x[i] * shift)

        return sum(shifts) * 100

    except Exception as e:
        print(e)
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