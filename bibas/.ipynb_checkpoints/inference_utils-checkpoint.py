import pandas as pd
from pgmpy.inference import VariableElimination, CausalInference

def compute_bibas_pairwise(model, source, target, target_positive_state=1, operation="observe"):
    """
    Compute the BIBAS score from source → target (target must be binary).
    
    Parameters:
        model: DiscreteBayesianNetwork
        source: str – source variable
        target: str – target variable (must be binary)
        target_positive_state: int – the index of the 'positive' state in the target (default=1)
        operation: 'observe' or 'do'
    
    Returns:
        float – BIBAS score (0–100), or None if computation fails
    """
    try:
        source_cpd = model.get_cpds(source)
        target_cpd = model.get_cpds(target)

        if target_cpd.variable_card != 2:
            raise ValueError("Target must be binary")

        # Prior probability of T+
        prior_infer = VariableElimination(model)
        p_t_pos = prior_infer.query(variables=[target]).values[target_positive_state]

        # Prior probabilities of source variable for weighting
        p_x = prior_infer.query(variables=[source]).values

        shifts = []

        if operation == "observe":
            infer = prior_infer
            for i in range(source_cpd.variable_card):
                posterior = infer.query(variables=[target], evidence={source: i})
                p_t_given_x = posterior.values[target_positive_state]
                shifts.append(p_x[i] * abs(p_t_given_x - p_t_pos))

        elif operation == "do":
            if target in model.get_parents(source):
                return 0.0  # Causal influence from child to parent is undefined, treated as 0
            infer = CausalInference(model)
            for i in range(source_cpd.variable_card):
                interventional = infer.query(variables=[target], do={source: i})
                p_t_given_x = interventional.values[target_positive_state]
                shifts.append(p_x[i] * abs(p_t_given_x - p_t_pos))

        else:
            raise ValueError("operation must be 'observe' or 'do'")

        return sum(shifts) * 100

    except Exception as e:
        print(f"[BIBAS Error] {e}")
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