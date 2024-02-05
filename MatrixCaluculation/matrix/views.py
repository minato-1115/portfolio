from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'matrix/index.html')

def calculate(request):
    if request.method == 'POST':
        selected_size_str = request.POST.get('table_size')
        logger.debug(f'table_size: {selected_size_str}')
        selected_size = int(selected_size_str) if selected_size_str is not None else 0 
        logger.debug(f'selected_size: {selected_size}')
        matrix = []
        for i in range(selected_size):
            row = []
            for j in range(selected_size):
                cell_id = f'cell_{i}_{j}'
                cell_value = float(request.POST.get(cell_id, 0))
                
                logger.debug(f'Cell Value ({i}, {j}): {cell_value}')

                try:
                    cell_value = float(cell_value)
                except ValueError:
                    logger.error('Error converting cell value to float')
                
                row.append(cell_value)
            matrix.append(row)
        matrix = np.array(matrix)
        if matrix.ndim == 1:
            matrix = matrix.reshape((1, -1))
        if matrix.shape[0] != matrix.shape[1]:
            return JsonResponse({'error': 'The matrix is not a square matrix'})

        determinant_result = calculate_determinant(matrix)
        inverse_matrix_result = calculate_inverse_matrix(matrix)
        

        return JsonResponse({
            'determinant_result': determinant_result,
            'inverse_matrix_result': inverse_matrix_result.tolist(),
            'original_matrix': matrix.tolist(),
        })

    # POST メソッド以外のリクエストにはエラーを返すか、適切な応答を返すことが望ましい
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def calculate_determinant(matrix):
    determinant = np.linalg.det(matrix)
    result_determiant = np.round(determinant, 3)
    return result_determiant
 

def calculate_inverse_matrix(matrix):
    try:
        inverse_matrix = np.linalg.inv(matrix)
        rounded_inverse_matrix = np.round(inverse_matrix, 2)
        return rounded_inverse_matrix
    except np.linalg.LinAlgError:
        return JsonResponse({'error': 'Error in calculating inverse matrix'}, status=400)