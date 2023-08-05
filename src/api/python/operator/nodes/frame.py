# -------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Modifications Copyright 2022 The DAPHNE Consortium
#
# -------------------------------------------------------------

__all__ = ["Frame"]

from api.python.operator.operation_node import OperationNode
from api.python.operator.nodes.scalar import Scalar
from api.python.operator.nodes.matrix import Matrix
from api.python.script_building.dag import OutputType
from api.python.utils.consts import VALID_INPUT_TYPES, VALID_ARITHMETIC_TYPES, BINARY_OPERATIONS, TMP_PATH

import pandas as pd

import json
import os
from typing import Union, TYPE_CHECKING, Dict, Iterable, Optional, Sequence, List

if TYPE_CHECKING:
    # to avoid cyclic dependencies during runtime
    from context.daphne_context import DaphneContext

class Frame(OperationNode):
    _pd_dataframe: pd.DataFrame
    _column_names: Optional[List[str]] = None

    def __init__(self, daphne_context: "DaphneContext", operation: str,
                 unnamed_input_nodes: Union[str, Iterable[VALID_INPUT_TYPES]] = None,
                 named_input_nodes: Dict[str, VALID_INPUT_TYPES] = None,
                 local_data: pd.DataFrame = None, brackets: bool = False, 
                 column_names: Optional[List[str]] = None) -> "Frame":
        is_python_local_data = False
        if local_data is not None:
            self._pd_dataframe = local_data
            is_python_local_data = True
        else:
            self._pd_dataframe = None

        self._column_names = column_names

        super().__init__(daphne_context, operation, unnamed_input_nodes,
                         named_input_nodes, OutputType.FRAME, is_python_local_data, brackets)

    def code_line(self, var_name: str, unnamed_input_vars: Sequence[str], named_input_vars: Dict[str, str]) -> str:
        if self.__copy:
            return f'{var_name}={unnamed_input_vars[0]};'
        code_line = super().code_line(var_name, unnamed_input_vars, named_input_vars).format(file_name=var_name, TMP_PATH = TMP_PATH) 
        
        #Save temporary csv file, if the operation is "readFrame"
        if self._is_pandas() and self.operation == "readFrame":
            self._pd_dataframe.to_csv(TMP_PATH+"/"+var_name+".csv", header=False, index=False)
            with open(TMP_PATH+"/"+var_name+".csv.meta", "w") as f:
                json.dump(
                    {
                        "numRows": self._pd_dataframe.shape[0],
                        "numCols": self._pd_dataframe.shape[1],
                        "schema": [
                            {
                                "label": self._pd_dataframe.columns[i],
                                "valueType": self.getDType(self._pd_dataframe.dtypes.iloc[i])
                            }
                            for i in range(self._pd_dataframe.shape[1])
                        ]
                    },
                    f, indent=2
                )
        return code_line

    def compute(self, type="shared memory", verbose=False, useIndexColumn=False) -> Union[pd.DataFrame]:
        return super().compute(type=type, verbose=verbose, useIndexColumn=useIndexColumn)

    def _is_pandas(self) -> bool:
        return self._pd_dataframe is not None

    def getDType(self, d_type):
        if d_type == "int64":
            return "si64"
        elif d_type == "float64":
            return "f64"
        else:
            print("Error")

    def rbind(self, other) -> 'Frame':
        """
        Row-wise frame concatenation, by concatenating the second frame as additional rows to the first frame. 
        :param: The other frame to bind to the right hand side
        :return: The OperationNode containing the concatenated frames.
        """
        return Frame(self.daphne_context, "rbind", [self, other])

    def cbind(self, other) -> 'Frame':
        """
        Column-wise frame concatenation, by concatenating the second frame as additional columns to the first frame. 
        :param: The other frame to bind to the right hand side.
        :return: The Frame containing the concatenated frames.
        """
        return Frame(self.daphne_context, "cbind", [self, other])

    def print(self):
        return OperationNode(self.daphne_context,'print',[self], output_type=OutputType.NONE)
        
    def cartesian(self, other) -> 'Frame':
        """
        cartesian product
        """
        return Frame(self.daphne_context, "cartesian", [self, other])
    
    def innerJoin(self, right_frame, left_on, right_on) -> 'Frame':
        """
        Creates an Inner Join between the object (left) and another frame (right)
        :param right_frame: Frame to join with the object
        :param left_on: Left Key (with left_on == right_on)
        :param right_on: Right Key (with left_on == right_on)
        :return: A Frame containing the Inner Join of both Frames.
        """
        return Frame(self.daphne_context, "innerJoin", [self, right_frame, left_on, right_on])

    def semiJoin(self, right_frame, left_on, right_on) -> 'Frame':
        """
        Creates a Semi Join between the object (left) and another frame (right)
        :param right_frame: Frame to join with the object
        :param left_on: Left Key (with left_on == right_on)
        :param right_on: Right Key (with left_on == right_on)
        :return: A Frame containing the Semi Join of both Frames.
        """
        return Frame(self.daphne_context, "semiJoin", [self, right_frame, left_on, right_on])
    
    def groupJoin(self, right_frame, left_on, right_on, right_Agg) -> 'Frame':
        """
        Creates a Group Join between the object (left) and another frame (right)
        :param right_frame: Frame to join with the object
        :param left_on: Left Key (with left_on == right_on)
        :param right_on: Right Key (with left_on == right_on)
        :param right_Agg: Aggregation Argument
        :return: A Frame containing the Group Join of both Frames.
        """
        return Frame(self.daphne_context, "groupJoin", [self, right_frame, left_on, right_on, right_Agg])
    
    def setColLabels(self, labels) -> 'Frame':
        """
        Changes the Column labels to the handed over labels.
        There must be as many labels as columns!
        :param labels: List of new labels
        :return: A Frame with the new labels
        """
        args = []
        args.append(self)
        numCols = self.ncol()

        if len(labels) == numCols:
            for label in labels: 
                label_str = f'"{label}"'
                args.append(label_str)

            return Frame(self.daphne_context, "setColLabels", args)
        else: 
            raise ValueError(f"Number of labels is not equal to the number of columns! \nExpected labels for {numCols} columns, but received {len(labels)} labels.")
    
    def setColLabelsPrefix(self, prefix) -> 'Frame':
        """
        Adds a Prefix to the labels of all columns
        :param prefix: Prefix to be added to every label
        :return: A Frame with updated labels
        """
        prefix_str=f'"{prefix}"'

        return Frame(self.daphne_context, "setColLabelsPrefix", [self, prefix_str])
    
    def toMatrix(self, data_type="f64") -> 'Matrix': 
        """
        Transforms the Frame to a Matrix of the type: data_type
        :param data_type: Data Type for the Matrix
        :return: A Matrix with the values of the datatype
        """
        return Matrix(self.daphne_context, f"as.matrix<{data_type}>", [self])
        
    def nrow(self) -> 'Scalar':
        """
        :return: Scalar containing number of rows of frame
        """
        return Scalar(self.daphne_context, 'nrow',[self])

    def ncol(self) -> 'Scalar':
        """
        :return: Scalar containing number of columns of frame
        """
        return Scalar(self.daphne_context, 'ncol',[self])

    def ncell(self) -> 'Scalar':
        return Scalar(self.daphne_context, 'ncell', [self])
    
    def order(self, colIdxs: List[int], ascs: List[bool], returnIndexes: bool) -> 'Frame':
        if len(colIdxs) != len(ascs):
            raise RuntimeError("order: the lists given for parameters colIdxs and ascs must have the same length")
        return Frame(self.daphne_context, 'order', [self, *colIdxs, *ascs, returnIndexes])

    def write(self, file: str) -> 'OperationNode':
        return OperationNode(self.daphne_context, 'writeFrame', [self,'\"'+file+'\"'], output_type=OutputType.NONE)