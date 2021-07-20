#!/usr/bin/env python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import kfp
from kfp import dsl
def myfun(a,b)->str:
    return str(int(a)+int(b));
my_op = kfp.components.func_to_container_op(myfun);
def split(text):
    return dsl.ContainerOp(
        name='txt-sp',
        image='python:3.7',
        command=['python3', '-c'],
        arguments=["import sys;m=sys.argv[1].split();f=open('/tmp/result','w');sys.stdout=f;print(m)",text],
        file_outputs={'out': '/tmp/result'},

        )
def com(t1,t2):
    return dsl.ContainerOp(
        name='con',
        image='star16231108/mypy:v1',
        command=["python3"],
        arguments=["/app/com.py",t1,t2],

        )
# def gcs_download_op(url):
#     return dsl.ContainerOp(
#         name='GCS - Download',
#         image='star16231108/cloud-sdk:279.0.0',
#         command=['sh', '-c'],
#         arguments=['gsutil cat $0 | tee $1', url, '/tmp/results.txt'],
#         file_outputs={
#             'data': '/tmp/results.txt',
#         }
#     )


def echo_op(text):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo "$0" |tee $1', text ,'/tmp/results.txt'],
        file_outputs={
            'data': '/tmp/results.txt',
        }
    )

def h():
    m=my_op(4,7);
    x=m.output;
    xx=my_op(x,x)
    return xx;
@dsl.pipeline(
    name='Sequential pipeline',
    description='A pipeline with two sequential steps.'
)
def sequential_pipeline(text='gs:// ml-pipeline/sample-data/ shakespeare/shakespeare1.txt'):
    """A pipeline with two sequential steps."""

    download_task = split(text)
    echo_task = echo_op(download_task.outputs['out'])
    mm=h()
    echo_task2 = echo_op(mm.output)
    com(str(echo_task.output),str(echo_task2.output))

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(sequential_pipeline, __file__ + '.yaml')
    client = kfp.Client(host='http://localhost:8082')
    client.create_run_from_pipeline_func(
    sequential_pipeline,
    arguments={
        'text': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    })
