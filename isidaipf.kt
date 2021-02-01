import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.select.Elements
import java.time.LocalDate
import java.time.LocalDateTime

abstract class Article(
        val document: Document
){
    abstract fun getHeadline() : String
    abstract fun getImages() : List<NewsImage>
    abstract fun getParagraphs(): List<String>
    abstract fun isLocal(): Boolean
    abstract fun getDate(): LocalDateTime
}
class NewsImage(
        val imageUrl: String,
        val caption: String

) {
    override fun toString(): String {
        return "NewsImage(imageUrl='$imageUrl', caption='$caption')"
    }
}
class StraitsArticle(document: Document) : Article(document){
    override fun getHeadline() : String
            = document.select("[itemprop=headline]").text()
    override fun getImages() : List<NewsImage>{
        val ele = document.select("img.img-responsive")
        return ele.map{NewsImage(it.attr("src"),it.attr("alt"))}.toList()
    }
    override fun getParagraphs(): List<String> {
        return document.select("[itemprop=articleBody]").first().getElementsByTag("p").map{it.text()}
    }
    override fun isLocal(): Boolean {
        return getParagraphs().first().startsWith("SINGAPORE")
    }
    override fun getDate(): LocalDateTime{
        val date = document.select("meta[property=og:updated_time]").attr("content")
        return LocalDateTime.parse(date)
    }
}

object Straits{
    val tagUrl = "https://www.straitstimes.com/tags/coronavirus"
    val articleUrl = "https://www.straitstimes.com"
    fun scrape_page_links(doc: Document)
        = doc.getElementsByClass("story-headline").map{
        articleUrl+it.getElementsByTag("a").attr("href")
    }
}

fun main(){
    val url: String = "https://www.straitstimes.com/tags/coronavirus"
    val article: String = "https://www.straitstimes.com/asia/east-asia/who-team-in-wuhan-to-visit-provincial-cdc-on-monday"
    val doc: Document = Jsoup.connect(url).get()
    println(StraitsArticle(Jsoup.connect(article).get()).getDate())
}
