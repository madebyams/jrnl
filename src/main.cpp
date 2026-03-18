#include "frontend_html.h"

#include <webview/webview.h>

#include <string>

int main()
{
    webview::webview w(false, nullptr);
    w.set_title("jrnl");
    w.set_size(1280, 800, WEBVIEW_HINT_NONE);
    w.set_html(std::string(jrnl::frontend_html));
    w.run();
    return 0;
}
