<?php

declare(strict_types=1);

namespace App\Formatters;

use InvalidArgumentException;

class TicketStatusFormatter
{
    private const STATUS_MAP = [
        'draft' => 'Draft Ticket',
        'published' => 'Published Ticket',
        'cancelled' => 'Cancelled Ticket',
    ];

    public function format(string $status): string
    {
        $statusKey = strtolower(trim($status));

        if (!array_key_exists($statusKey, self::STATUS_MAP)) {
            throw new InvalidArgumentException(sprintf('Unknown status: "%s"', $status));
        }

        return self::STATUS_MAP[$statusKey];
    }
}
