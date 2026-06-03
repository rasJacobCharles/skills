<?php

declare(strict_types=1);

namespace App\Handlers;

use App\Interfaces\PaymentServiceInterface;
use App\Interfaces\ViewRendererInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Laminas\Diactoros\Response\RedirectResponse;
use Laminas\Diactoros\Response\HtmlResponse;

class BoxOfficePaymentHandler
{
    private PaymentServiceInterface $paymentService;
    private ViewRendererInterface $viewRenderer;

    public function __construct(
        PaymentServiceInterface $paymentService,
        ViewRendererInterface $viewRenderer
    ) {
        $this->paymentService = $paymentService;
        $this->viewRenderer = $viewRenderer;
    }

    public function handle(ServerRequestInterface $request): ResponseInterface
    {
        $method = strtoupper($request->getMethod());

        if ($method === 'GET') {
            $html = $this->viewRenderer->render('payment_form', [
                'errors' => []
            ]);
            return new HtmlResponse($html);
        }

        if ($method === 'POST') {
            $params = $request->getParsedBody();
            $amount = isset($params['amount']) ? (float) $params['amount'] : 0.0;
            $token = $params['token'] ?? '';

            if ($amount <= 0.0 || empty($token)) {
                $html = $this->viewRenderer->render('payment_form', [
                    'errors' => ['Amount must be positive and payment token is required.']
                ]);
                return new HtmlResponse($html, 400);
            }

            $success = $this->paymentService->charge($amount, $token);

            if ($success) {
                return new RedirectResponse('/receipt');
            }

            $html = $this->viewRenderer->render('payment_form', [
                'errors' => ['Payment processing failed. Please try again.']
            ]);
            return new HtmlResponse($html, 500);
        }

        return new HtmlResponse('Method not allowed', 405);
    }
}
