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
# 30: except_star_with_group	
# 31: except_star_without_group
# 32: raised_exception_group
# 33: caught_exception_group
# 34: exception_groups
# 35: except_star_files
# 36: exception_group_files
# 37: structural_pattern_match
# 38: pattern_as
# 39: pattern_or
# 40: pattern_sequence
# 41: pattern_mapping
# 42: pattern_class
# 43: pattern_value
# 44: pattern_singleton
# 45: pattern_star
# 46: structural_pattern_match_files
# 47: pattern_as_files
# 48: pattern_or_files
# 49: pattern_sequence_files
# 50: pattern_mapping_files
# 51: pattern_class_files
# 52: pattern_value_files
# 53: pattern_singleton_files
# 54: pattern_star_files
# 55: assign_unpack
# 56: list_unpack
# 57: tuple_unpack
# 58: set_unpack
# 59: dict_unpack
# 60: call_kwargs_unpack
# 61: call_args_unpack
# 62: assign_unpack_files
# 63: list_unpack_files
# 64: tuple_unpack_files
# 65: set_unpack_files
# 66: dict_unpack_files
# 67: call_kwargs_unpack_files
# 68: call_args_unpack_files
# 69: nonlocal
# 70: nonlocal_files
# 71: function_args_annotation
# 72: function_return_annotation
# 73: function_args_annotation_files
# 74: function_return_annotation_files
# 75: kw_defaults
# 76: kw_args
# 77: kw_defaults_files
# 78: kw_args_files
# 79: type_vars_bounds
# 81: type_vars_constraints
# 82: type_param_spec
# 83: type_var_tuple
# 84: type_alias
# 85: type_vars_bounds_files
# 86: type_vars_constraints_files
# 87: type_param_spec_files
# 88: type_var_tuple_files
# 89: type_alias_files
# 90: type_hint_list
# 91: type_hint_tuple
# 92: type_hint_dict
# 93: type_hint_set
# 94: type_hint_frozenset
# 95: type_hint_type
# 96: type_hint_list_files
# 97: type_hint_tuple_files
# 98: type_hint_dict_files
# 99: type_hint_set_files
# 100: type_hint_frozenset_files
# 101: type_hint_type_files
# 102: statements
# 103: errors

# Atribui os argumentos a variáveis
STRING_DATA=$1
NUMERO_COLUNA=$2
VALOR_COLUNA=$3

# Executa o comando awk com os argumentos fornecidos
# Exemplo sh filter_feature_first_occurrence.sh 2012-01 5 1

awk -F, -v date="$STRING_DATA" -v col="$NUMERO_COLUNA" -v val="$VALOR_COLUNA" '
BEGIN {OFS = FS}
NR == 1 {print; next}
$2 ~ date && $col >= val' filtered-results.csv > feature_first_occurrences.csv
