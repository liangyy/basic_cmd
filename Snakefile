rule all:
    input:
        expand('{out_dir}/{{data}}.fastq.gz'.format(out_dir=config['out_dir']), data=config['SRR_id'])

rule fetch:
    params:
        srr = lambda wildcards: config['SRR_id'][wildcards.data],
        dir = config['out_dir']
    log:
        'logs/{data}.log'
    output:
        '{out_dir}/{data}.fastq.gz'
    shell:
        'fastq-dump -O {params.dir} --gzip {params.srr} 2> {log}'
