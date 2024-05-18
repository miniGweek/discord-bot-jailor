using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Bot.Discord.Jailor.Service
{
    public class Service : IHostedService
    {
        private readonly ILogger<Service> _logger;

        public Service(ILogger<Service> logger)
        {
            _logger = logger;
        }
        async Task IHostedService.StartAsync(CancellationToken cancellationToken)
        {
            await Task.Delay(1000, cancellationToken);
            _logger.LogInformation("Starting ....");
            while (true)
            {
                _logger.LogInformation("Running ....");
                await Task.Delay(1000);
            }
        }

        async Task IHostedService.StopAsync(CancellationToken cancellationToken)
        {
            await Task.Delay(1000, cancellationToken);
            _logger.LogInformation("Stopping ....");
        }
    }
}
