using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web.Http;

namespace Forward.Controllers
{
    public class DefaultController : ApiController
    {
        
    }

    public class ProxyHandler : DelegatingHandler
    {
        protected override async System.Threading.Tasks.Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, System.Threading.CancellationToken cancellationToken)
        {
            try
            {
                UriBuilder forwardUri = new UriBuilder(request.RequestUri);
                //strip off the proxy port and replace with an Http port
                forwardUri.Port = 5000;
                forwardUri.Host = "localhost";
                //send it on to the requested URL
                request.RequestUri = forwardUri.Uri;
                HttpClient client = new HttpClient();
                if (request.Method == HttpMethod.Get || request.Method == HttpMethod.Head)
                {
                    request.Content = null;
                }
                var response = Task.Run(() => client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead)).Result;
                return response;
            }
            catch (Exception e)
            {
                return null;
            }
        }
    }
}
