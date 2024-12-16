import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    total_prob = 1  # Initialize the total probability to 1

    for person in people:
        # Get the mother and father of the current person
        mother = people[person]['mother']
        father = people[person]['father']

        # Determine the number of genes the person has
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        else:
            num_genes = 0

        # Calculate the probability of having the number of genes
        if mother is None and father is None:
            # If there are no parents listed, use the unconditional probability
            gene_prob = PROBS['gene'][num_genes]
        else:
            # If parents are listed, calculate the probability based on parents' genes
            probs_from_mother = {
                2: 1 - PROBS['mutation'],  # Probability mother passes the gene if she has 2 copies
                1: 0.5,                    # Probability mother passes the gene if she has 1 copy
                0: PROBS['mutation']       # Probability mother passes the gene if she has 0 copies (mutation)
            }
            probs_from_father = {
                2: 1 - PROBS['mutation'],  # Probability father passes the gene if he has 2 copies
                1: 0.5,                    # Probability father passes the gene if he has 1 copy
                0: PROBS['mutation']       # Probability father passes the gene if he has 0 copies (mutation)
            }

            # Probability of getting the gene from mother
            if people[mother]['name'] in two_genes:
                mother_prob = probs_from_mother[2]
            elif people[mother]['name'] in one_gene:
                mother_prob = probs_from_mother[1]
            else:
                mother_prob = probs_from_mother[0]

            # Probability of getting the gene from father
            if people[father]['name'] in two_genes:
                father_prob = probs_from_father[2]
            elif people[father]['name'] in one_gene:
                father_prob = probs_from_father[1]
            else:
                father_prob = probs_from_father[0]

            # Calculate gene probability based on inheritance and mutations
            if num_genes == 2:
                gene_prob = mother_prob * father_prob
            elif num_genes == 1:
                gene_prob = mother_prob * (1 - father_prob) + (1 - mother_prob) * father_prob
            else:
                gene_prob = (1 - mother_prob) * (1 - father_prob)

        # Calculate the probability of having or not having the trait
        trait_prob = PROBS['trait'][num_genes][person in have_trait]

        # Update the total probability with the current person's probability
        total_prob *= gene_prob * trait_prob

    return total_prob  # Return the joint probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        # Update gene probability
        if person in two_genes:
            probabilities[person]["gene"][2] += p  # If person has two genes, add p to the probability of having 2 genes
        elif person in one_gene:
            probabilities[person]["gene"][1] += p  # If person has one gene, add p to the probability of having 1 gene
        else:
            probabilities[person]["gene"][0] += p  # If person has no genes, add p to the probability of having 0 genes

        # Update trait probability
        if person in have_trait:
            probabilities[person]["trait"][True] += p  # If person has the trait, add p to the probability of having the trait
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_p_genes = sum(probabilities[person]["gene"].values())
        total_p_trait = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= total_p_genes

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= total_p_trait


if __name__ == "__main__":
    main()
