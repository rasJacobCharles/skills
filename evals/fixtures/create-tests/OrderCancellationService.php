<?php

declare(strict_types=1);

namespace App\Services;

use App\Exceptions\OrderAlreadyCancelledException;
use App\Interfaces\OrderRepositoryInterface;
use App\Interfaces\RefundGatewayInterface;
use App\Models\Order;

class OrderCancellationService
{
    private OrderRepositoryInterface $orderRepository;
    private RefundGatewayInterface $refundGateway;

    public function __construct(
        OrderRepositoryInterface $orderRepository,
        RefundGatewayInterface $refundGateway
    ) {
        $this->orderRepository = $orderRepository;
        $this->refundGateway = $refundGateway;
    }

    public function cancelOrder(int $orderId): bool
    {
        $order = $this->orderRepository->find($orderId);
        
        if ($order === null) {
            return false;
        }

        if ($order->isCancelled()) {
            throw new OrderAlreadyCancelledException($orderId);
        }

        $refundSuccess = $this->refundGateway->refund($orderId, $order->getAmount());

        if (!$refundSuccess) {
            return false;
        }

        $order->setCancelled(true);
        $this->orderRepository->save($order);

        return true;
    }
}
