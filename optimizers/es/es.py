import numpy as np

from optimizers.core.optimizer import Optimizer


class ES(Optimizer):
    """Evolution Strategies (ES).

    Reference
    ---------
    Hansen, N., Arnold, D.V. and Auger, A., 2015.
    Evolution strategies.
    In Springer Handbook of Computational Intelligence (pp. 871-898). Springer, Berlin, Heidelberg.
    https://link.springer.com/chapter/10.1007%2F978-3-662-43505-2_44

    http://www.scholarpedia.org/article/Evolution_strategies

    Beyer, H.G. and Schwefel, H.P., 2002.
    Evolution strategies–A comprehensive introduction.
    Natural Computing, 1(1), pp.3-52.
    https://link.springer.com/article/10.1023/A:1015059928466

    Schwefel, H.P., 1984.
    Evolution strategies: A family of non-linear optimization techniques based on
        imitating some principles of organic evolution.
    Annals of Operations Research, 1(2), pp.165-167.
    https://link.springer.com/article/10.1007/BF01876146
    """
    def __init__(self, problem, options):
        Optimizer.__init__(self, problem, options)
        if self.n_individuals is None:  # offspring population size (λ: lambda)
            self.n_individuals = 4 + int(3 * np.log(self.ndim_problem))
        if self.n_parents is None:  # parent population size (μ: mu)
            self.n_parents = int(self.n_individuals / 2)
            if self.n_parents > 0:
                w_base, w = np.log((self.n_individuals + 1) / 2), np.log(np.arange(self.n_parents) + 1)
                self._w = (w_base - w) / (self.n_parents * w_base - np.sum(w))
                self._mu_eff = 1 / np.sum(np.power(self._w, 2))  # μ_eff / μ_w
        self.mean = options.get('mean')  # mean of Gaussian search distribution
        if self.mean is None:  # 'mean' has priority over 'x'
            self.mean = options.get('x')
        self.sigma = options.get('sigma')  # global step-size (σ)
        self.eta_mean = options.get('eta_mean')  # learning rate of mean
        self.eta_sigma = options.get('eta_sigma')  # learning rate of std
        self._n_generations = 0
        # for restart
        self.n_restart = 0
        self._sigma_bak = np.copy(self.sigma)
        self.sigma_threshold = options.get('sigma_threshold', 1e-10)
        self._fitness_list = [self.best_so_far_y]  # store best_so_far_y generated in each generation
        self.stagnation = options.get('stagnation', self.n_individuals * 100)
        self.fitness_diff = options.get('fitness_diff', 1e-20)

    def initialize(self):
        raise NotImplementedError

    def iterate(self):
        raise NotImplementedError

    def _initialize_mean(self, is_restart=None):
        if (is_restart is True) or (self.mean is None):
            mean = self.rng_initialization.uniform(self.initial_lower_boundary,
                                                   self.initial_upper_boundary)
        else:
            mean = np.copy(self.mean)
        return mean

    def _print_verbose_info(self, y):
        if self.verbose and (not self._n_generations % self.verbose_frequency):
            best_so_far_y = -self.best_so_far_y if self._is_maximization else self.best_so_far_y
            info = '  * Generation {:d}: best_so_far_y {:7.5e}, min(y) {:7.5e} & Evaluations {:d}'
            print(info.format(self._n_generations, best_so_far_y, np.min(y), self.n_function_evaluations))

    def restart_initialize(self):
        self._fitness_list.append(self.best_so_far_y)
        is_restart = self.sigma < self.sigma_threshold
        if len(self._fitness_list) >= self.stagnation:
            is_restart_2 = (self._fitness_list[-self.stagnation] - self._fitness_list[-1]) < self.fitness_diff
        else:
            is_restart_2 = False
        is_restart = is_restart or is_restart_2
        if is_restart:
            is_restart = True
            self.n_restart += 1
            self.sigma = np.copy(self._sigma_bak)
            self.n_individuals *= 2
            self.n_parents = int(self.n_individuals / 2)
            w_base, w = np.log((self.n_individuals + 1) / 2), np.log(np.arange(self.n_parents) + 1)
            self._w = (w_base - w) / (self.n_parents * w_base - np.sum(w))
            self._mu_eff = 1 / np.sum(np.power(self._w, 2))
            self._fitness_list = [np.Inf]
        return is_restart

    def _collect_results(self, fitness):
        results = Optimizer._collect_results(self, fitness)
        results['mean'] = self.mean
        results['sigma'] = self.sigma
        results['_n_generations'] = self._n_generations
        results['n_restart'] = self.n_restart
        return results
