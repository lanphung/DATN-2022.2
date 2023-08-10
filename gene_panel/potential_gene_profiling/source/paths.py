import os
import string
source_path = os.path.dirname(__file__)
BASE_path = os.path.dirname(source_path)

class MyDict(dict):
    def __init__(self, *args, **kw):
        super(MyDict,self).__init__(*args, **kw)
        self.itemlist = super(MyDict,self).keys()
        self.fmt = string.Formatter() 

    def __getitem__(self, item):
        return self.fmt.vformat(dict.__getitem__(self, item), {}, self)
dyes_no = {
    'yes': '1',
    'no': '0'
}
dpaths = MyDict({
    # base_paths
    'base': BASE_path,
    'source': '{base}/source',
    'resource': '{base}/resource',
    'output': '{base}/output',
    'classification': '{resource}/classification.csv',
    # classifer outputs
    'classifier': '{output}/classifier.csv',
    'nci': '{output}/nci.csv',
    # COSMIC paths
    'v98g37': '/media/data3/biodataset/COSMIC/v98/GRCh37',
    'csample': '{v98g37}/CosmicSample.tsv',
    'cmexport': '{v98g37}/CosmicMutantExport.tsv',
    'action': '{v98g37}/ActionabilityData.tsv',
    'resist': '{v98g37}/CosmicResistanceMutations.tsv',
    # sample output
    'msample': '{output}/targeted_sample.csv',
    'asample': '{output}/targeted_asian_sample.csv',
    'wgen': '{output}/gen_set.csv',
    'agen': '{output}/asian_gen_set.csv',
    # other source output
    'name': '{output}/nci_and_name.csv',
    # coding point mutation output
    'mcmexport': '{output}/targeted_mutation.csv',
    'acmexport': '{output}/targeted_asian_mutant.csv', #asian coding point muts
    'sup_codmut': '{output}/targeted_mutation_sup.csv',
    'sup_acodmut': '{output}/targeted_asian_mutant_sup.csv',
    # actionablity output
    'maction': '{output}/action.csv',
    # resistance output
    'mresist': '{output}/resist.csv',
    # output by class
    'lung': '{output}/lung',
    'breast': '{output}/breast',
    'thyroid': '{output}/thyroid',
    'colorectal': '{output}/colorectal',
    'hepatocellular': '{output}/hepatocellular',
    # individual output
    'indiv': '{output}/individual.csv',
})
