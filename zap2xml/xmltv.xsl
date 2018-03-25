<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.1">
    <xsl:output method="html" />

    <!-- Sorting keys -->
    <xsl:key name="channel_key" match="programme" use="@channel"/>
    <xsl:key name="date_key" match="programme" use="substring(@start,1,8)"/>
    <xsl:key name="channel_date_key" match="programme" use="concat(@channel, ',', substring(@start,1,8))"/>

    <!-- Main Template: Build the Framework of the Page -->
    <xsl:template match="/">
        <html>
            <head>
                <link rel="stylesheet" href="xmltv.css" type="text/css" />
                <link rel="stylesheet" href="programme_categories.css" type="text/css" />
                <title>TV Listings (TEST)</title>
            </head>
            <body>
                <h1>TV Listing</h1>
<!-- TBD MGouin:
                <xsl:apply-templates select="/tv" mode="normal"/>
-->
                <xsl:apply-templates select="/tv" mode="key"/>
            </body>
        </html>
    </xsl:template>  <!-- end match="/" -->

    <!-- ******************************************************************************** -->
    <xsl:template match="tv" mode="normal">
        <h2>Template tv normal</h2>
        <xsl:apply-templates select="channel" mode="full" />
<!-- TBD MGouin:
        <xsl:apply-templates select="channel" mode="full" />
        <xsl:apply-templates select="channel" mode="simple" />
        <xsl:apply-templates select="programme" mode="full" />
        <xsl:apply-templates select="programme" mode="simple" />
-->
    </xsl:template>  <!-- end match="tv" -->

    <!-- ******************************************************************************** -->
    <xsl:template match="tv" mode="key">
        <h2>Template tv key</h2>
        <ul>
            <xsl:apply-templates mode="channel_group" select="
                programme[
                  generate-id()
                  =
                  generate-id(
                    key('channel_key', @channel)[1]
                  )
                ]
              ">
            </xsl:apply-templates>
        </ul>
    </xsl:template>  <!-- end match="tv" -->

    <!-- ******************************************************************************** -->
    <xsl:template match="channel" mode="full">
        <h3>
            <xsl:value-of select="display-name[1]"/> |
            <xsl:value-of select="@id" />
        </h3>

        <xsl:variable name="chanid" select="@id" />
        <xsl:for-each select="/tv/programme[@channel=$chanid]">
            <xsl:sort select="@start" data-type="text" order="ascending" />
<!-- TBD MGouin:
            <div><xsl:value-of select="title" /></div>
-->
            <xsl:apply-templates select="." mode="simple" />
        </xsl:for-each>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="channel" mode="simple">
        <h3>
            <xsl:value-of select="display-name[1]"/> |
            <xsl:value-of select="@id" />
        </h3>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="programme" mode="full">
        <xsl:variable name="category_class">
            <xsl:call-template name="convert_category">
                <xsl:with-param name="value" select="category/text()"/>
            </xsl:call-template>
        </xsl:variable>
        <div class="{$category_class}">
            <h3>
            <xsl:value-of select="title" />
            </h3>
            <div>
                Ch: <xsl:value-of select="@channel" />
            </div>
            <div>
                [<xsl:value-of select="@start" />] to [<xsl:value-of select="@stop" />]
            </div>
            <div>
                Description: <xsl:value-of select="desc" />
            </div>
            <div>
                Category: <xsl:value-of select="category" />
            </div>
            <div>
                Ep: <xsl:value-of select="episode-num" />
            </div>
        </div>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="programme" mode="simple">
        <xsl:variable name="start_time" select="concat(substring(@start,9,2), ':', substring(@start,11,2))" />
        <xsl:variable name="stop_time"  select="concat(substring(@stop,9,2), ':', substring(@stop,11,2))" />
        <xsl:variable name="start_date" select="concat(substring(@start,1,4), '-', substring(@start,5,2), '-', substring(@start,7,2))" />

        <xsl:variable name="category_class">
            <xsl:call-template name="convert_category">
                <xsl:with-param name="value" select="category/text()"/>
            </xsl:call-template>
        </xsl:variable>

        <div class="{$category_class}">
            programme simple: <xsl:value-of select="$start_date" />
            [<xsl:value-of select="$start_time" />-<xsl:value-of select="$stop_time" />]
            <xsl:value-of select="title" />
        </div>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="programme" mode="simple_no_date">
        <xsl:variable name="start_time" select="concat(substring(@start,9,2), ':', substring(@start,11,2))" />
        <xsl:variable name="stop_time"  select="concat(substring(@stop,9,2), ':', substring(@stop,11,2))" />

        <xsl:variable name="category_class">
            <xsl:call-template name="convert_category">
                <xsl:with-param name="value" select="category/text()"/>
            </xsl:call-template>
        </xsl:variable>

        <li>
            <div class="{$category_class}">
                [<xsl:value-of select="$start_time" />-<xsl:value-of select="$stop_time" />]
                <xsl:value-of select="title" />
            </div>
        </li>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="programme" mode="channel_group">
        <xsl:variable name="chanid" select="@channel" />
        <li>
            <xsl:value-of select="/tv/channel[@id=$chanid]/display-name[1]" />
            <!-- TBD MGouin:
            http://stackoverflow.com/questions/948218/xslt-3-level-grouping-on-attributes/955527
            http://www.jenitennison.com/xslt/grouping/muenchian.html
            -->

            <ul>
                <xsl:apply-templates mode="date_group" select="
                  key('channel_key', @channel)[
                    generate-id()
                    =
                    generate-id(
                      key(
                        'channel_date_key',
                        concat(
                            @channel,
                            ',',
                            substring(@start,1,8))
                      )[1]
                    )
                  ]
                ">
                    <xsl:sort select="substring(@start,1,14)" data-type="number" />
                </xsl:apply-templates>
            </ul>
        </li>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template match="programme" mode="date_group">
        <xsl:variable name="start_date" select="concat(substring(@start,1,4), '-', substring(@start,5,2), '-', substring(@start,7,2))" />
        <li>
            <xsl:value-of select="$start_date" />
            <ul>
                <xsl:apply-templates mode="simple_no_date" select="
                  key(
                    'channel_date_key',
                    concat(
                        @channel,
                        ',',
                        substring(@start,1,8)
                    )
                  )
                  ">
                  <xsl:sort select="@start" data-type="text" />
                </xsl:apply-templates>
            </ul>
        </li>
    </xsl:template>

    <!-- ******************************************************************************** -->
    <xsl:template name="convert_category">
        <xsl:param name="value" />
        <xsl:choose>
            <xsl:when test="$value != ''"> <!-- Category provided -->
                <xsl:variable name="apos" select='"&apos;"'/>
                <xsl:choose>
                    <xsl:when test="$value = concat('Children', $apos, 's / Youth programmes')">
                        child
                    </xsl:when>
                    <xsl:when test="$value = 'Movie / Drama'">
                        drama
                    </xsl:when>
                    <xsl:when test="$value = 'News / Current affairs'">
                        news
                    </xsl:when>
                    <xsl:when test="$value = 'Show / Game show'">
                        serie
                    </xsl:when>
                    <xsl:when test="$value = 'Sports'">
                        sport
                    </xsl:when>
                    <xsl:otherwise>
                        unknown
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                empty_category
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
