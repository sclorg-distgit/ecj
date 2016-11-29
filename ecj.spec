%{?scl:%scl_package ecj}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Epoch: 1

%global qualifier R-4.6-201606061100

Summary: Eclipse Compiler for Java
Name: %{?scl_prefix}ecj
Version: 4.6
Release: 1.%{baserelease}%{?dist}
URL: http://www.eclipse.org
License: EPL

Source0: http://download.eclipse.org/eclipse/downloads/drops4/%{qualifier}/ecjsrc-%{version}.jar
Source1: ecj.sh.in
Source3: https://repo1.maven.org/maven2/org/eclipse/jdt/core/compiler/ecj/%{version}/ecj-%{version}.pom
# Extracted from https://www.eclipse.org/downloads/download.php?file=/eclipse/downloads/drops4/%%{qualifier}/ecj-%%{version}.jar
Source4: MANIFEST.MF

# Always generate debug info when building RPMs (Andrew Haley)
Patch0: %{pkg_name}-rpmdebuginfo.patch

BuildArch: noarch

BuildRequires: gzip
BuildRequires: %{?scl_prefix_java_common}ant
BuildRequires: %{?scl_prefix_maven}javapackages-local

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q -c
%patch0 -p1

sed -i -e 's|debuglevel=\"lines,source\"|debug=\"yes\"|g' build.xml
sed -i -e "s/Xlint:none/Xlint:none -encoding cp1252/g" build.xml

cp %{SOURCE3} pom.xml
mkdir -p scripts/binary/META-INF/
cp %{SOURCE4} scripts/binary/META-INF/MANIFEST.MF

# JDTCompilerAdapter isn't used by the batch compiler
rm -f org/eclipse/jdt/core/JDTCompilerAdapter.java

# No dep on ant needed
%pom_remove_dep org.apache.ant:ant

# Symlinks and aliases
%mvn_file :ecj ecj eclipse-ecj jdtcore
%mvn_alias org.eclipse.jdt.core.compiler:ecj \
  org.eclipse.tycho:org.eclipse.jdt.core org.eclipse.tycho:org.eclipse.jdt.compiler.apt \
  org.eclipse.jetty.orbit:org.eclipse.jdt.core org.eclipse.jetty.orbit:org.eclipse.jdt.compiler.apt \
  org.eclipse.jdt:core
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
ant 
gzip ecj.1
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_artifact pom.xml ecj.jar
%mvn_install

# Install the ecj wrapper script
install -p -D -m0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ecj

# Install manpage
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p ecj.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/ecj.1.gz
%{?scl:EOF}


%files -f .mfiles
%doc about.html
%{_bindir}/ecj
%{_mandir}/man1/ecj*

%changelog
* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 1:4.6-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Fri Jul 01 2016 Mat Booth <mat.booth@redhat.com> - 1:4.6-1
- Update to Neon release

* Tue Apr 26 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5.2-3
- Re-add alias for org.eclipse.jdt:core

* Fri Apr 22 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.2-2
- Drop aliases that are now provided by eclipse-jdt

* Mon Feb 29 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.2-1
- Update to Mars.2 release

* Fri Feb 05 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.1-3
- Allow any compression man pages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Mat Booth <mat.booth@redhat.com> - 1:4.5.1-1
- Update to Mars.1 release

* Thu Jul 2 2015 Alexander Kurtakov <akurtako@redhat.com> 1:4.5-1
- Update to upstream 4.5 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Mat Booth <mat.booth@redhat.com> - 1:4.4.2-1
- Update to 4.4.2.
- Install with mvn_install
- Add jetty.orbit alias
- Add compiler.apt aliases
- Drop ancient obsoletes/provides on eclipse-ecj
- Use man page from upstream source

* Thu Jan 8 2015 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.1-1
- Update to 4.4.1.

* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-1
- Update to 4.4 final.
- Drop gcj patches as gcj is not in Fedora anymore and ecj now requires 1.6.

* Thu Jun 12 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.4.git20140430
- Add additional depmap for maven.

* Mon Jun 9 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.3.git20140430
- Fix FTBFS.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.0-0.2.git20140430
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 1 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.1.git20140430
- Update to 4.4.0 I-build to make it cope with Java 8.

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1:4.2.1-10
- Drop gcj AOT-compilation support.
- Obsolete -native sub-package.

* Wed Oct 09 2013 gil cattaneo <puntogil@libero.it> 1:4.2.1-9
- enable build of org/eclipse/jdt/internal/compiler/[apt,tool]
  (ant build mode only), required by querydsl
- remove some rpmlint problems (invalid date)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Jon VanAlten <jon.vanalten@redhat.com> - 4.2.1-7
- Add manpage for ecj executable
- Resolves: rhbz#948442

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-6
- Add depmap for org.eclipse.jdt.core.compiler:ecj
- Resolves: rhbz#949938

* Wed Mar 06 2013 Karsten Hopp <karsten@redhat.com> 1:4.2.1-5
- add BR java-devel for !with_gcjbootstrap

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-3
- Patch GCCMain to avoid dummy symbols.

* Wed Oct 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.2.1-2
- Add depmap satysfying Tycho req.

* Sun Jul 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-1
- Update to 4.2.1 upstream version.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-13
- Add missing epoch to native subpackage requires.

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-12
- Separate gcj in subpackage.

* Mon Jan 16 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-11
- Patch pom file to better represent ecj and not jdt.core .
- Guidelines fixes.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.4.2-8
- Fix add_to_maven_depmap call (Resolves rhbz#655796)

* Mon Dec 21 2009 Deepak Bhole <dbhole@redhat.com> - 1:3.4.2-7
- Fix RHBZ# 490936. If CLASSPATH is not set, add . to default classpath.

* Wed Sep 9 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-6
- Add maven pom and depmaps.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-4
- Add patch to generate full debuginfo for ecj itself

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-3
- Add BR for aot-compile-rpm

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-2
- Add BR for ant

* Fri Mar 6 2009 Andrew Overholt <overholt@redhat.com> 1:3.4.2-1
- 3.4.2

* Tue Dec 9 2008 Andrew Overholt <overholt@redhat.com> 1:3.4.1-1
- 3.4.1
- Don't conditionalize building of gcj AOT bits (we're only building
  this for gcj and IcedTea bootstrapping).

* Mon Jan 22 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- Add eclipse-ecj-gcj.patch.

* Fri Jan 12 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- First version for Fedora 7.
- Add BR: java-devel for jar.

* Thu Nov 02 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.1-1jpp
- First version for JPackage.

* Mon Jul 24 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- Add versionless ecj.jar symlink in /usr/share/java.

* Wed Jul 19 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- 3.2.0.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.9
- Don't build for ppc or ia64.

* Sun Feb 20 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.6
- Upgrade back to 3.1M4.
- Don't build for i386 and x86_64.
- Provide eclipse-ecj until we can deprecate this package.

* Fri Jan 14 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.4
- build for all but x86

* Thu Jan 13 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.3
- build for ppc exclusively

* Wed Jan 12 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.2
- Add RPM_OPT_FLAGS workaround.

* Tue Jan 11 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.1
- New version.

* Mon Sep 27 2004 Gary Benson <gbenson@redhat.com> 2.1.3-5
- Rebuild with new katana.

* Thu Jul 22 2004 Gary Benson <gbenson@redhat.com> 2.1.3-4
- Build without bootstrap-ant.
- Split out lib-org-eclipse-jdt-internal-compiler.so.

* Tue Jul  6 2004 Gary Benson <gbenson@redhat.com> 2.1.3-3
- Fix ecj-devel's dependencies.

* Wed Jun  9 2004 Gary Benson <gbenson@redhat.com> 2.1.3-2
- Work around an optimiser failure somewhere in ecj or gcj (#125613).

* Fri May 28 2004 Gary Benson <gbenson@redhat.com>
- Build with katana.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com> 2.1.3-1
- Initial Red Hat Linux build.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com>
- Upgraded to latest version.

* Sun Jul 20 2003 Anthony Green <green@redhat.com>
- Add %%doc

* Fri Jul 18 2003 Anthony Green <green@redhat.com>
- Initial RHUG build.