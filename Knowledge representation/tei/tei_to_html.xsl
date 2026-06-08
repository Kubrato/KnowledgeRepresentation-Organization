<?xml version="1.0" encoding="UTF-8"?>

<!-- ============================================================
     TEI -> HTML transformation
     This stylesheet reads the TEI file (encoding.xml) and turns it
     into a simple, readable HTML web page (encoding.html).
     Run it with:  xsltproc tei_to_html.xsl encoding.xml > encoding.html
     ============================================================ -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">

  <!-- We want HTML (not XML) as the final output, encoded in UTF-8. -->
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- ============================================================
       MAIN TEMPLATE: matches the root <TEI> element.
       It builds the whole HTML page skeleton (html/head/body).
       ============================================================ -->
  <xsl:template match="/tei:TEI">
    <html>
      <head>
        <!-- The page <title> is taken from the TEI <title> in the header. -->
        <title><xsl:value-of select="tei:teiHeader//tei:titleStmt/tei:title"/></title>
        <!-- A tiny bit of styling so the annotated entities stand out. -->
        <style>
          body { font-family: sans-serif; max-width: 700px; margin: 40px auto; line-height: 1.6; }
          .entity { font-weight: bold; }
          .quote  { font-style: italic; color: #555; }
        </style>
      </head>
      <body>
        <!-- Big page heading = the TEI title. -->
        <h1><xsl:value-of select="tei:teiHeader//tei:titleStmt/tei:title"/></h1>
        <!-- Now process the text body (the divs with the Wikipedia excerpts). -->
        <xsl:apply-templates select="tei:text/tei:body"/>
      </body>
    </html>
  </xsl:template>

  <!-- ============================================================
       Each <div> in the body becomes a section.
       Its <head> becomes an <h2>, and its <p> becomes a paragraph.
       <xsl:apply-templates> means "keep processing what is inside".
       ============================================================ -->
  <xsl:template match="tei:div">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- A TEI <head> (section heading) -> HTML <h2>. -->
  <xsl:template match="tei:head">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>

  <!-- A TEI <p> (paragraph) -> HTML <p>. -->
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <!-- ============================================================
       ENTITY ANNOTATIONS.
       In the TEI text, real-world entities are tagged with
       <persName>, <placeName>, <orgName>, <title> and <rs>.
       Here we turn each of them into a <span> shown in bold,
       so the reader can SEE which words were annotated as entities.
       ============================================================ -->
  <xsl:template match="tei:persName | tei:placeName | tei:orgName | tei:title | tei:rs">
    <span class="entity"><xsl:apply-templates/></span>
  </xsl:template>

  <!-- A quotation <quote> -> shown in italics. -->
  <xsl:template match="tei:quote">
    <span class="quote"><xsl:apply-templates/></span>
  </xsl:template>

</xsl:stylesheet>
