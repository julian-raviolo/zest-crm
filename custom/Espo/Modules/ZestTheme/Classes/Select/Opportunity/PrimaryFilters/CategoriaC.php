<?php

namespace Espo\Modules\ZestTheme\Classes\Select\Opportunity\PrimaryFilters;

use Espo\Core\Select\Primary\Filter;
use Espo\ORM\Query\SelectBuilder;

/** Filtro rápido: leads con categoría C. */
class CategoriaC implements Filter
{
    public function apply(SelectBuilder $queryBuilder): void
    {
        $queryBuilder->where(['categoria' => 'C']);
    }
}
