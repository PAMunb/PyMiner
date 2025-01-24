#!/bin/bash

# Verifica se o número correto de argumentos foi fornecido
if [ "$#" -ne 3 ]; then
    echo "Uso: $0 <string_data> <numero_da_coluna> <valor_na_coluna>"
    exit 1
fi

# Número das colunas no CSV
# 1: project
# 2: date
# 3: commit_hash
# 4: files
# 5: dict_union
# 6: dict_union_update
# 7: dict_union_files
# 8: dict_union_update_files
# 9: async_list_comprehensions
# 10: async_set_comprehensions
# 11: async_dict_comprehensions
# 12: async_generator_expressions
# 13: async_list_comprehensions_files
# 14: async_set_comprehensions_files
# 15: async_dict_comprehensions_files
# 16: async_generator_expressions_files
# 17: matrix_multiplication
# 18: matrix_multiplication_files
# 19: async_def
# 20: await_expressions
# 21: async_for
# 22: async_with
# 23: async_def_files
# 24: await_expressions_files
# 25: async_for_files
# 26: async_with_files
# 27: fstring
# 28: fstring_files
# 29: except_star
# 30: except_star_files
# 31: structural_pattern_match
# 32: pattern_as
# 33: pattern_or
# 34: pattern_sequence
# 35: pattern_mapping
# 36: pattern_class
# 37: pattern_value
# 38: pattern_singleton
# 39: pattern_star
# 40: structural_pattern_match_files
# 41: pattern_as_files
# 42: pattern_or_files
# 43: pattern_sequence_files
# 44: pattern_mapping_files
# 45: pattern_class_files
# 46: pattern_value_files
# 47: pattern_singleton_files
# 48: pattern_star_files
# 49: assign_unpack
# 50: list_unpack
# 51: tuple_unpack
# 52: set_unpack
# 53: dict_unpack
# 54: call_kwargs_unpack
# 55: call_args_unpack
# 56: assign_unpack_files
# 57: list_unpack_files
# 58: tuple_unpack_files
# 59: set_unpack_files
# 60: dict_unpack_files
# 61: call_kwargs_unpack_files
# 62: call_args_unpack_files
# 63: nonlocal
# 64: nonlocal_files
# 65: function_args_annotation
# 66: function_return_annotation
# 67: function_args_annotation_files
# 68: function_return_annotation_files
# 69: kw_defaults
# 70: kw_args
# 71: kw_defaults_files
# 72: kw_args_files
# 73: type_vars_bounds
# 74: type_vars_constraints
# 75: type_param_spec
# 76: type_var_tuple
# 77: type_alias
# 78: type_vars_bounds_files
# 79: type_vars_constraints_files
# 80: type_param_spec_files
# 81: type_var_tuple_files
# 82: type_alias_files
# 83: type_hint_list
# 84: type_hint_tuple
# 85: type_hint_dict
# 86: type_hint_set
# 87: type_hint_frozenset
# 88: type_hint_type
# 89: type_hint_list_files
# 90: type_hint_tuple_files
# 91: type_hint_dict_files
# 92: type_hint_set_files
# 93: type_hint_frozenset_files
# 94: type_hint_type_files
# 95: statements
# 96: errors

# Atribui os argumentos a variáveis
STRING_DATA=$1
NUMERO_COLUNA=$2
VALOR_COLUNA=$3

# Executa o comando awk com os argumentos fornecidos
# Exemplo sh sh filter_feature_first_occurrence.sh 2012-01 5 1

awk -F, -v date="$STRING_DATA" -v col="$NUMERO_COLUNA" -v val="$VALOR_COLUNA" '
BEGIN {OFS = FS}
NR == 1 {print; next}
$2 ~ date && $col >= val' filtered-results.csv > feature_first_occurrences.csv
