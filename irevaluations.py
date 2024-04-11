

def fscore(beta, retrieved_docs, relevant_docs):
    retrieved = set(retrieved_docs)
    relevant = set(relevant_docs)

    tp = len(retrieved.intersection(relevant))

    precision = tp / len(retrieved)
    recall = tp / len(relevant)

    result = (1 + (beta ** 2)) / (((beta ** 2) / recall) + (1 / precision))

    print(f"Retrieved and relevant: {tp} docs - {retrieved.intersection(relevant)}")
    print(f"Precision = {tp} / {len(retrieved)} = {round(precision, 3)}")
    print(f"Recall = {tp} / {len(relevant)} = {round(recall, 3)}")
    print(f"F({beta}) score = (1 + ({beta} ^ 2)) / ((({beta} ^ 2) / {round(recall, 3)}) "
          f"+ (1 / {round(precision, 3)})) = {round(result, 3)}\n")

    return result


def kendalls_tau(ideal, candidate):
    assert len(ideal) == len(candidate)

    ideal_pairs = []
    candidate_pairs = []

    # agreements = []
    # disagreements = []


    ideal_indexes = {i: ideal.index(i) for i in ideal}
    candidate_indexes = {i: candidate.index(i) for i in candidate}

    for i in range(len(ideal)):
        for j in range(i + 1, len(ideal)):

            ideal_pairs.append((ideal[i], ideal[j]))
            candidate_pairs.append((candidate[i], candidate[j]))

            # if candidate_indexes[ideal[i]] < candidate_indexes[ideal[j]]:
            #     agreements.append((i, j))
            # else:
            #     disagreements.append((i, j))

    agreements = set(candidate_pairs).intersection(ideal_pairs)
    disagreements = set(candidate_pairs).difference(ideal_pairs)

    result = (len(agreements) - len(disagreements)) / (len(agreements) + len(disagreements))

    print(f"All ideal pairs: {ideal_pairs}")
    print(f"All candidate pairs: {candidate_pairs}")
    print(f"There are {len(agreements)} agreements: {agreements}")
    print(f"There are {len(disagreements)} disagreements: {disagreements}")
    print(f"Kendall's tau = ({len(agreements)} - {len(disagreements)}) / ({len(agreements)} + {len(disagreements)}) = {round(result, 3)}\n")

    return result


def main():
    retrieved = [1, 2, 3, 4, 5, 6]
    relevant = [1, 3, 5, 7, 9]

    fscore(0.5, retrieved, relevant)
    fscore(1, retrieved, relevant)
    fscore(1.5, retrieved, relevant)

    # ideal = [4, 2, 3, 5, 1]
    # candidate = [5, 4, 2, 3, 1]

    ideal = [1, 2, 3, 4, 5, 6]
    candidate = [2, 3, 4, 5, 1, 6]

    kendalls_tau(ideal, candidate)

if __name__ == "__main__":
    main()
