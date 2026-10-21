def bayes_posterior(prior,p_flag_given_yes,p_flag_given_no):
    p_opposite = 1- prior

    p_spam_flagged = prior * p_flag_given_yes
    p_notspam_flagged = p_opposite * p_flag_given_no
    all_flagged = p_spam_flagged + p_notspam_flagged

    return p_spam_flagged/all_flagged

def cdf(probs):
    running_sum = 0
    res_cdf = []
    for num in probs:
        running_sum = running_sum + num
        res_cdf.append(running_sum)

    return res_cdf

def expectation(values,probs):
    exp = 0
    for value,prob in zip(values,probs):
        exp += value * prob

    return exp

def variance(values,probs):
    exp = expectation(values,probs)
    var = 0
    for value,prob in zip(values,probs):
        var += (value-exp)**2 * prob

    return var